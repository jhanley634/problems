// Copyright 2022 John Hanley. MIT licensed.

use pyo3::prelude::{PyModule, PyResult, Python, pyfunction, pymodule, wrap_pyfunction};
use std::fs::File;
use std::io::{BufRead, BufReader, Read};
use std::str;

#[pyfunction]
fn load_txt(path: &str) -> PyResult<Vec<f64>> {
    // This consumes ~ 150 .CSV files per second.
    // A hint of Vec::with_capacity(13000) instead of new() lets it hit 160 per sec.
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
    return second.parse::<f64>().unwrap();
}

#[pyfunction]
fn buffered_load_txt(path: &str) -> PyResult<Vec<f64>> {
    // This only consumes ~ 50 .CSV files per second.
    let mut ret = Vec::new();
    let infile = BufReader::new(File::open(path)?);
    for line1 in infile.lines() {
        if let Ok(line) = line1 {
            ret.push(second_num(&line));
        }
    }
    Ok(ret)
}

#[pymodule]
fn rust_fast(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_txt, m)?)?;
    m.add_function(wrap_pyfunction!(buffered_load_txt, m)?)?;
    Ok(())
}
