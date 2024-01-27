
use std::io::{self, Write};

fn get_input() -> String {
    print!("Plain text:  ");
    io::stdout().flush().unwrap();

    let mut buf = String::new();
    io::stdin().read_line(&mut buf).unwrap();
    buf
}


fn main() {
    let i = 42;
    println!("Hello, world!");
    let line = get_input();
    println!(">{}<", line.trim_end());
    println!("{}", i);
}
