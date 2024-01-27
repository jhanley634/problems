//! Copyright 2024 John Hanley. MIT licensed.

use std::io::{self};

use regex::Regex;

/// Returns a line from stdin.
/// It will typically end with \n.
/// A zero-length result means EOF.
fn read_line() -> String {
    let mut buffer = String::new();
    io::stdin().read_line(&mut buffer).unwrap();
    buffer
}

/// Filter that emulates `/bin/cat -n`.
fn _cat_n() {
    let mut i = 0;
    loop {
        let line = read_line();
        if line.is_empty() {
            break;
        }
        i += 1;
        println!("{:>6}  {}", i, line.trim_end());
    }
}

/// Filter that emulates `tr A-Z a-z`.
fn downcase_stdin() {
    loop {
        let line = read_line();
        if line.is_empty() {
            break;
        }
        _downcase_line(line);
    }
}

fn _downcase_line(line: String) {
    let upper_re = Regex::new(r"([A-Z])").unwrap();
    let mut i = 0;
    let mut r: std::ops::Range<usize>;
    let s = line.as_str();
    for m in upper_re.find_iter(s) {
        r = m.range();
        assert!(r.len() == 1);
        if r.start > i {
            print!("{}", &s[i..r.start])
        }
        i = r.end;
        print!("{}", s[r].to_string().to_ascii_lowercase())
    }
    if i < s.len() {
        print!("{}", &s[i..s.len()])
    }
}

fn main() {
    downcase_stdin()
}
