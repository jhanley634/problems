
use std::io::{self, Write};

fn get_input() -> String {
    io::stdout().flush().unwrap();
    let mut buffer = String::new();
    io::stdin().read_line(&mut buffer).unwrap();
    buffer
}

/// Filter that emulates `/bin/cat -n`.
fn cat_n() {
    let mut i = 0;
    let mut line;
    line = get_input();
    while !line.is_empty() {
        i += 1;
        println!("{:>6}  {}", i, line.trim_end());
        line = get_input();
    }
}

fn main() {
    cat_n()
}
