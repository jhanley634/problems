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
    let upper_re = Regex::new(r"([A-Z])").unwrap();
    loop {
        let line = read_line();
        if line.is_empty() {
            break;
        }
        print!("{}", _downcase_line(line, &upper_re))
    }
}

fn _downcase_line(line: String, upper_re: &Regex) -> String {
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

fn main() {
    downcase_stdin()
}
