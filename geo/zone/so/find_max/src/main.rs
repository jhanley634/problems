// Copyright 2023 John Hanley. MIT licensed.

use rand::Rng;

fn main() {
    find_max()
}

fn find_max() {
    let xs = [0.2, 1., 0.3];
    let max = xs
        .into_iter()
        .max_by(|a, b| a.partial_cmp(b).unwrap())
        .unwrap();
    // let integer_max = xs.iter().copied().max().unwrap();
    println!("x {} y {:?} z", max, xs);

    let num = rand::thread_rng().gen_range(0..100);
    println!("{}", num);
}
