use std::io::Read;
use std::str;
use pyo3::prelude::*;


#[pyfunction]
fn load_txt(filename: &str) -> PyResult<f64> {
    let mut file = std::fs::File::open(filename).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    let mut lines = contents.lines();
    let line = lines.next().unwrap();
    // let num = line.parse::<f64>().unwrap();
    // Ok(num)
    let e = 2.7182818284590452353602874713527;
    let p = 3.1415926535897932384626433832795;
    Ok(e + p)
}

#[pymodule]
fn rust_fast(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_txt, m)?)?;
    Ok(())
}
