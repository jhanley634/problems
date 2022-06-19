// Copyright 2022 John Hanley. MIT licensed.

use std::fs::File;
use std::io::Read;
use std::str;
use pyo3::prelude::{PyModule, PyResult, Python, pyfunction, pymodule, wrap_pyfunction};


#[pyfunction]
fn load_txt(path: &str) -> PyResult<Vec<f64>> {
    let mut infile = File::open(path).unwrap();
    let mut content = String::new();
    infile.read_to_string(&mut content).unwrap();
    let mut ret = Vec::new();
    for line in content.lines() {
        ret.push(second_num(line));
    }
    Ok(ret)
}


fn second_num(line: &str) -> f64 {
    // e.g. "7  8" --> 8.0
    let mut words = line.split_whitespace();
    words.next();  // discard first word
    let second = words.next().unwrap();
    return second.parse::<f64>().unwrap()
}


#[pymodule]
fn rust_fast(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_txt, m)?)?;
    Ok(())
}
