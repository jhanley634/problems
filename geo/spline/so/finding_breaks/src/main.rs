use parquet::file::reader::{FileReader, SerializedFileReader};

use parquet::record::RowAccessor;

use std::error::Error;
use std::fs::File;

fn read_parquet_file(file_path: &str) -> Result<Vec<i16>, Box<dyn Error>> {
    let file = File::open(file_path)?;

    // Create a Parquet file reader
    let reader = SerializedFileReader::new(file)?;

    let row_iter = reader.get_row_iter(None)?;

    let schema = reader.metadata().file_metadata().schema();
    let num_columns = schema.get_fields().len();
    println!("Found {} columns", num_columns);

    let mut xs = Vec::new();

    // Iterate over the rows and extract the integer values
    for row in row_iter {
        let row = row?;
        if row.len() > 0 {
            let x_value: i16 = row.get_short(0).unwrap();
            xs.push(x_value);
        }
    }
    Ok(xs)
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = "/tmp/sorted_xs.parquet";

    // Read in the "x" integer values
    let xs = read_parquet_file(file_path)?;

    // Print out the values
    println!("{:?}", xs);
    Ok(())
}
