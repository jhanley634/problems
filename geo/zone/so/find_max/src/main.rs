// Copyright 2023 John Hanley. MIT licensed.

use ordered_float::OrderedFloat;
// use std::f32::NAN;
use rand::Rng;
use std::time::Instant;

const N: usize = 1_000_000;

fn main() {
    sorted(roll_randoms());
    let xs = roll_randoms();
    find_max(xs);
}

fn sorted(mut xs: Vec<OrderedFloat<f32>>) -> Vec<OrderedFloat<f32>> {
    xs.sort_by(|a, b| a.partial_cmp(b).unwrap());
    xs
}

// fn convert(xs: Vec<f32>) -> Vec<OrderedFloat<f32>> {
//     xs as Vec<OrderedFloat<f32>>
// }

fn find_max(xs: Vec<OrderedFloat<f32>>) {
    let t0 = Instant::now();
    let max = xs.iter().max_by(|a, b| a.partial_cmp(b).unwrap()).unwrap();
    // let integer_max = xs.iter().copied().max().unwrap();
    let elapsed = t0.elapsed();

    println!("found {} in {:.6} seconds", max, elapsed.as_secs_f64());

    let num = rand::thread_rng().gen_range(0.1f32..0.3f32);

    println!("{}\t{}", num, num.sqrt());
}

fn roll_randoms() -> Vec<OrderedFloat<f32>> {
    let mut rng = rand::thread_rng();
    let mut xs = vec![OrderedFloat(0.0f32); 10 * N];
    for i in 0..N {
        xs[i] = OrderedFloat(rng.gen_range(0.0..1.0));
    }
    xs
}
