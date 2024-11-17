use parquet::file::reader::{FileReader, SerializedFileReader};
use parquet::record::RowAccessor;
use std::error::Error;
use std::fs::File;

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

fn main() -> Result<(), Box<dyn Error>> {
    let xs = read_parquet_file("/tmp/sorted_xs.parquet")?;
    println!("{:?}", xs);
    Ok(())
}
