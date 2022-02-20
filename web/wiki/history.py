#! /usr/bin/env python
# Copyright 2021 John Hanley. MIT licensed.
"""
Retrieves article history from Wikipedia's RESTful API.
"""
from pathlib import Path
import datetime as dt
import re
import subprocess

from glom import glom
import click
import requests

utc = dt.timezone.utc


class HistoryScraper:

    def __init__(self, title: str):
        assert '/' not in title, title
        assert re.search(r'^[\w()-]+$', title), title
        self.page_url_prefix = f'https://en.wikipedia.org/w/rest.php/v1/page/{title}'
        self.title = title

    @staticmethod
    def get(url: str):
        headers = {
            'User-Agent': 'jhanley634-history-scraper-v1'
        }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp

    @staticmethod
    def _minor(is_minor: bool):
        return 'm' if is_minor else '.'

    author_re = re.compile(r'([\w .-]+)')

    @classmethod
    def _get_author(cls, rev: dict):
        name = glom(rev, 'user.name')
        name = cls.author_re.search(name).group(1).strip()  # Sanitize.
        assert name, rev  # Wikipedia requires a non-empty author name.
        pseudo_email = f"<{name.replace(' ', '_')}@wiki>"
        return f'{name} {pseudo_email}'  # Git requires Ident + email addr, so dup it.

    older_re = re.compile(r'/history\?older_than=\d+$')

    def _get_reverse_history_ids(self):
        # now = int(dt.datetime.now(tz=dt.timezone.utc).timestamp())
        older = f'{self.page_url_prefix}/history'
        while older:
            d = self.get(older).json()
            for rev in d['revisions']:
                minor = 'm' if rev['minor'] else ' '
                yield (rev['id'],
                       dt.datetime.fromisoformat(rev['timestamp'].removesuffix('Z')).replace(tzinfo=utc),
                       self._get_author(rev),
                       f"{minor} {rev['comment']}".strip() or '.')
            older = d.get('older')
            if older:
                assert self.older_re.search(older), older

    def _get_all_history_ids(self):
        return sorted(self._get_reverse_history_ids())

    @staticmethod
    def _short_lines(txt: str) -> str:
        txt = txt.replace('\n', '\n\n======\n')  # This improves `diff` output a bit.
        txt = txt.replace('<', '\n<')
        # Line break, for diff, on a deterministic subset of words. (Nothing special about "vowels".)
        txt = re.sub(r'([aeiou])', r'\n\1', txt, re.IGNORECASE)
        lines = [line.strip()  # so `git log -p` won't append EOL red "trailing blank" notations
                 for line in txt.split('\n')]
        return '\n'.join(lines)

    def write_versions(self, out_dir=Path('/tmp/wiki_history')):
        out_dir.mkdir(exist_ok=True)
        git_dir = out_dir / '.git'
        if not git_dir.exists():
            cmd = f'cd {out_dir} && git init'
            subprocess.check_call(cmd, shell=True)
            assert git_dir.exists()

        comment_re = re.compile(r'^([()[\]\w  !#$%&*+,./:;<=>?@^~{|}–-]*)')

        for id_, stamp, author, comment in self._get_all_history_ids():
            stamp = stamp.strftime('%Y-%m-%dT%H:%M:%S')
            comment = comment.replace('"', '.').replace("'", '.')
            out_file = out_dir / self.title
            out_file_id = Path(f'{out_file}-{id_}')
            if not out_file_id.exists():
                resp = self.get(f'https://en.wikipedia.org/w/index.php?title={self.title}&oldid={id_}')
                msg_file = Path('/tmp/commit-message.txt')
                with open(msg_file, 'w') as fout:
                    fout.write(f'{stamp}\n')
                    fout.write(f'{comment}')
                with open(out_file_id, 'w') as fout:
                    fout.write(resp.text)
                with open(out_file, 'w') as fout:
                    fout.write(self._short_lines(resp.text))
                m = comment_re.search(comment)
                if comment != m.group(1):
                    print(comment)
                    print(m.group(1))
                print(author, '.')
                cmd = f'''
                    cd {out_dir} &&
                    git add {self.title} &&
                    git commit --date={stamp} --author "{author}" -m "{comment}"'''
                subprocess.check_call(cmd, shell=True)


@click.command()
@click.option('--article-url', default='Nathan_Safir')
def main(article_url):
    prefix = 'https://en.wikipedia.org/wiki/'  # We strip the prefix if present, for copy-n-paste convenience
    HistoryScraper(article_url.replace(prefix, '')).write_versions()


if __name__ == '__main__':
    main()
