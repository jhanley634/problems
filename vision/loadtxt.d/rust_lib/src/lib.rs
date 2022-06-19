use std::fs::File;
use std::io::Read;
use std::str;
use pyo3::prelude::*;
// use pyo3::types::{PyList, PyTuple};


#[pyfunction]
fn load_txt(path: &str) -> PyResult<Vec<f64>> {
    let mut infile = File::open(path).unwrap();
    let mut s = String::new();
    infile.read_to_string(&mut s).unwrap();
    let mut v = Vec::new();
    for line in s.lines() {
        for field in line.split_whitespace().collect::<Vec<_>>() {
            v.push(field.parse::<f64>().unwrap());
        }
    }
    Ok(v)
}


#[pyfunction]
fn read_number_pairs(filename: &str) -> PyResult<f64> {
    let mut f = std::fs::File::open(filename).unwrap();
    let mut contents = String::new();
    f.read_to_string(&mut contents).unwrap();
    // let mut lines = contents.lines();
    // for line in lines.iter() {
    //     let mut words = line.split_whitespace();
    //     let first = words.next().unwrap();
    //     let second = words.next().unwrap();
    //     let first_num = first.parse::<f64>().unwrap();
    //     let second_num = second.parse::<f64>().unwrap();
    //     return Ok(first_num + second_num);
    // }
    Ok(0.0)
}



#[pymodule]
fn rust_fast(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_txt, m)?)?;
    Ok(())
}
