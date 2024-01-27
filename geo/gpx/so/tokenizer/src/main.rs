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
        for (_, [upper]) in upper_re.captures_iter(line.as_str()).map(|c| c.extract()) {
            println!("{}.", upper.to_string().to_lowercase())
        }
    }
}

fn main() {
    downcase_stdin()
}
