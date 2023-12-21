use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Extrapolate values based on problem description.
fn extrapolate_value(seq: Vec<i64>) -> i64 {
    let diffs = seq
        .iter()
        .tuple_windows()
        .map(|(a, b)| (*b) - (*a))
        .collect::<Vec<i64>>();

    let last = *(seq.get(seq.len() - 1).expect("Sequence must have at least one element."));

    if diffs.iter().all(|d| (*d) == 0) {
        last
    } else {
        last + extrapolate_value(diffs)
    }
}

fn solution_p1(input: String) -> i64 {

    let mut total = 0;

    for line in input.lines() {
        let nums = line
            .split(' ')
            .filter(|s| (*s).len() > 0)
            .map(|s| s.parse::<i64>().expect("Must be valid number."))
            .collect::<Vec<i64>>();

        total += extrapolate_value(nums);
    }
    
    total

}


/// Extrapolate values backwards based on problem description.
fn extrapolate_value_backwards(seq: Vec<i64>) -> i64 {
    let diffs = seq
        .iter()
        .tuple_windows()
        .map(|(a, b)| (*b) - (*a))
        .collect::<Vec<i64>>();

    let first = *(seq.get(0).expect("Sequence must have at least one element."));

    if diffs.iter().all(|d| (*d) == 0) {
        first
    } else {
        first - extrapolate_value_backwards(diffs)
    }
}

fn solution_p2(input: String) -> i64 {

    let mut total = 0;

    for line in input.lines() {
        let nums = line
            .split(' ')
            .filter(|s| (*s).len() > 0)
            .map(|s| s.parse::<i64>().expect("Must be valid number."))
            .collect::<Vec<i64>>();

        total += extrapolate_value_backwards(nums);
    }
    
    total

}


#[cfg(test)]
mod tests {
    use crate::day9::{solution_p1, solution_p2};

    const EXAMPLE: &str = "0 3 6 9 12 15\n1 3 6 10 15 21\n10 13 16 21 30 45\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 114);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 2);
    }
}
