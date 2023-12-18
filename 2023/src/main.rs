use std::env;
use std::fs;

mod day1;

fn run_day_main(day: u8, part2: bool, input: String) {
    match day {
        1 => day1::solution(input, part2),
        _ => eprintln!("Invalid day!")
    }
}

fn run_solution(day: u8, part2: bool) {
    let input = fs::read_to_string(format!("./inputs/{}.txt", day));
    match input {
        Ok(s) => run_day_main(day, part2, s),
        Err(e) => eprintln!("{e}")
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let day = &args[1].parse::<u8>();
    let part2 = &args[2].parse::<u8>();

    match day {
        Ok(d) => {
            match part2 {
                Ok(p2) => run_solution(*d, *p2 == 2 as u8),
                Err(e) => eprintln!("{e}"),
            }
        },
        Err(e) => eprintln!("{e}"),
    }
}
