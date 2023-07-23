// Copyright 2023 John Hanley. MIT licensed.

// use ordered_float::OrderedFloat;
// use std::f32::NAN;
use rand::Rng;
use std::time::Instant;

const N: usize = 100_000;

fn main() {
    let xs = sorted(roll_randoms());
    find_max(xs);
}

fn sorted(mut xs: [f32; N]) -> [f32; N] {
    // let mut xs = vec![xs_in];
    // xs_in.clone();
    xs.sort_by(|a, b| a.partial_cmp(b).unwrap());
    xs
}

// fn convert(xs: Vec<[f32; N]>) -> Vec<OrderedFloat<[f32; N]>> {
//     xs as Vec<OrderedFloat<[f32; N]>>
// }

fn find_max(xs: [f32; N]) {
    let t0 = Instant::now();
    let max = xs
        .into_iter()
        .max_by(|a, b| a.partial_cmp(b).unwrap())
        .unwrap();
    // let integer_max = xs.iter().copied().max().unwrap();
    let elapsed = t0.elapsed();

    println!("found {} in {:.6} seconds", max, elapsed.as_secs_f64());

    let num = rand::thread_rng().gen_range(0.1f32..0.3f32);

    println!("{}\t{}", num, num.sqrt());
}

fn roll_randoms() -> [f32; N] {
    let xs: [f32; N] = [(); N].map(|_| rand::thread_rng().gen_range(0.0..1.0));
    return xs;
}
