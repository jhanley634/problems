use parquet::file::reader::{FileReader, SerializedFileReader};
use parquet::record::RowAccessor;
use std::error::Error;
use std::fs::File;
use std::time::Instant;
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

fn main() -> Result<(), Box<dyn Error>> {
    let now = Instant::now();
    let xs = read_parquet_file("/tmp/sorted_xs.parquet")?;
    println!("{:.3}", now.elapsed().as_secs_f32());

    let million_sum = 5_504_562;
    let ten_million_sum = 55_008_083;
    let sec = timeit_loops!(1, {
        let s = sum_int16(&xs);
        assert!(s == million_sum || s == ten_million_sum);
    });
    println!("{:.4}", sec);
    Ok(())
}
