//! Copyright 2024 John Hanley. MIT licensed.

use std::io::{self};

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
    let mut line;
    line = read_line();
    while !line.is_empty() {
        i += 1;
        println!("{:>6}  {}", i, line.trim_end());
        line = read_line();
    }
}

fn main() {
    cat_n()
}
