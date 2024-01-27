//! Copyright 2024 John Hanley. MIT licensed.

use std::io::{self};

// use regex::Regex;

/// Returns a line from stdin.
/// It will typically end with \n.
/// A zero-length result means EOF.
fn read_line() -> String {
    let mut buffer = String::new();
    io::stdin().read_line(&mut buffer).unwrap();
    buffer
}

/// Filter that emulates `/bin/cat -n`.
fn cat_n() {
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
    // let upper_re = Regex::new(r"[A-Z]").unwrap();
    let mut line;
    line = read_line();
    while !line.is_empty() {
        line = read_line();
    }
}

fn main() {
    cat_n()
}
