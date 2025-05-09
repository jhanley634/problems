use parquet::file::reader::{FileReader, SerializedFileReader};
use parquet::record::RowAccessor;
use std::error::Error;
use std::fs::File;
use timeit::timeit_loops;

fn read_parquet_file(file_path: &str) -> Result<Vec<i16>, Box<dyn Error>> {
    let file = File::open(file_path)?;
    let reader = SerializedFileReader::new(file)?;
    let row_iter = reader.get_row_iter(None)?;

    let schema = reader.metadata().file_metadata().schema();
    let num_columns = schema.get_fields().len();
    assert_eq!(1, num_columns);

    // Read each value.
    let mut xs = Vec::new();
    for row in row_iter {
        let x_value: i16 = row?.get_short(0).unwrap();
        xs.push(x_value);
    }
    Ok(xs)
}

fn sum_int16(xs: &[i16]) -> i64 {
    xs.iter().map(|&x| x as i64).sum()
}

/// Finds an xs index where the element values change.
fn find_break(xs: &[i16], start: usize, end: usize) -> usize {
    assert!(!xs.is_empty());
    let mut i = start;
    let mut j = end;
    assert!(i < j);

    while i < j {
        let mid = i + (j - i) / 2;
        if xs[i] == xs[mid] {
            i = mid + 1;
        } else {
            j = mid;
        }
    }
    assert!(i == 0 || xs[i - 1] != xs[i]);
    println!("at i = {}:\t{},\t{}", i, xs[i - 1], xs[i]);

    i
}

#[macro_use]
extern crate timeit;

fn main() -> Result<(), Box<dyn Error>> {
    timeit!({
        let in_file = "/tmp/sorted_xs.parquet";
	println!("reading {} ...", in_file);
        let xs = read_parquet_file(in_file)?;

        let million_sum = 5_504_562;
        let ten_million_sum = 55_008_083;
        sum_int16(&xs); // Warm the cache.
        let sec = timeit_loops!(1, {
            let s = sum_int16(&xs);
            assert!(s == million_sum || s == ten_million_sum);
        });
        println!("sum_int16() took {:.4} s", sec);

        let br = find_break(&xs, 0, xs.len());
        println!("Break at {}", br);
    });
    Ok(())
}
