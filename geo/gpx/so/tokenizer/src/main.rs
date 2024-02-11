//! Copyright 2024 John Hanley. MIT licensed.

use lazy_regex::{regex, Lazy};
use regex::Regex;
use std::io::{self, BufRead, BufReader};

/// Returns a line from stdin.
/// It will typically end with \n.
/// A zero-length result means EOF.
fn _read_line() -> String {
    let mut buffer = String::new();
    io::stdin().read_line(&mut buffer).unwrap();
    buffer
}

/// Filter that emulates `/bin/cat -n`.
fn _cat_n() {
    let mut i = 0;
    loop {
        let line = _read_line();
        if line.is_empty() {
            break;
        }
        i += 1;
        println!("{:>6}  {}", i, line.trim_end());
    }
}

/// Filter that emulates `tr A-Z a-z`.
fn _downcase_stdin() {
    let _upper_re = Regex::new(r"([A-Z])").unwrap();
    loop {
        let line = _read_line();
        if line.is_empty() {
            break;
        }
        print!("{}", _downcase_line(line))
        // print!("{}", _downcase_line_with_regex(line, &_upper_re))
    }
}

fn _downcase_line(line: String) -> String {
    line.to_ascii_lowercase()
}

fn _downcase_line_by_char_slowly(line: String) -> String {
    let mut result = String::new();
    for ch in line.chars() {
        if ch.is_uppercase() {
            result += &ch.to_ascii_lowercase().to_string()
        } else {
            result += &ch.to_string()
        }
    }
    result
}

fn _downcase_line_with_regex(line: String, upper_re: &Regex) -> String {
    let mut result = String::new();
    let mut i = 0;
    let mut r: std::ops::Range<usize>;
    let s = line.as_str();
    for m in upper_re.find_iter(s) {
        r = m.range();
        assert!(r.len() == 1);
        if r.start > i {
            result += &s[i..r.start]
        }
        i = r.end;
        result += s[r].to_string().to_ascii_lowercase().as_str()
    }
    if i < s.len() {
        result += &s[i..s.len()]
    }
    result
}

fn tokenize_stdin() {
    let stdin = BufReader::new(io::stdin());
    for line in stdin.lines() {
        for word in _tokenize_line(line.unwrap()).split_whitespace() {
            print!("{}\n", word)
        }
    }
}

static _PUNCTUATION_RE: &Lazy<Regex> = regex!(r#"([.,;:!?”'"()\[\]{}_-])"#);

fn _tokenize_line(line: String) -> String {
     _PUNCTUATION_RE.replace_all(&line, " ").to_lowercase()
 }

fn main() {
    tokenize_stdin()
}
