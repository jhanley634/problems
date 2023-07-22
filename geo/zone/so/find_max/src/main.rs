// Copyright 2023 John Hanley. MIT licensed.

use rand::Rng;

const N: usize = 100_000;

fn main() {
    let xs = roll_randoms();
    find_max(xs);
}

fn find_max(xs: [f32; N]) {
    let max = xs
        .into_iter()
        .max_by(|a, b| a.partial_cmp(b).unwrap())
        .unwrap();
    // let integer_max = xs.iter().copied().max().unwrap();
    println!("x {} y", max);

    let num = rand::thread_rng().gen_range(0.1f32..0.3f32);

    println!("{}\t{}", num, num.sqrt());
}

fn roll_randoms() -> [f32; N] {
    let xs: [f32; N] = [(); N].map(|_| rand::thread_rng().gen_range(0.0..1.0));
    return xs;
}
