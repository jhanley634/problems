// Copyright 2023 John Hanley. MIT licensed.

// https://codereview.stackexchange.com/questions/284186/rust-book-exercise

use std::collections::HashMap;

fn main() {
    use itertools::Itertools;
    let mut v = vec![10, -1, 9, -2];
    println!("{}", exercise_median_of_vector(&mut v));
    println!("{v:?}");
    let perms = v.iter().permutations(v.len());
    println!("{:?}", perms.clone().collect::<Vec<_>>());
    println!("{perms:?}");
    for perm in perms {
        println!("{perm:?}");
    }

    let v = vec![1, 2, 3, 1];
    println!("{}", exercise_mode_of_vector(&v));
}

fn exercise_median_of_vector(v: &mut Vec<i32>) -> i32 {
    v.sort();

    let half = v.len() / 2;

    if (half & 1) == 1 {
        v[half + 1]
    } else {
        v[half]
    }
}

fn exercise_mode_of_vector(vector: &Vec<i32>) -> i32 {
    struct Highest {
        key: i32,
        count: i32,
    }

    let mut mode = HashMap::new();
    let mut highest = Highest { key: 0, count: 0 };

    for key in vector {
        let count = mode.entry(key).or_insert(0);
        *count += 1;

        if *count > highest.count {
            highest.count = *count;
            highest.key = *key;
        }
    }

    highest.key
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_median() {
        use itertools::Itertools;
        let v = vec![10, -1, 9, -2];
        for perm in v.clone().iter().permutations(v.len()) {
            println!("{perm:?}");
        }
        assert_eq!(9, exercise_median_of_vector(&mut v.to_vec()));
    }
    #[test]
    fn test_mode() {
        let v = vec![1, 2, 3, 1];
        assert_eq!(1, exercise_mode_of_vector(&v));
    }
}
