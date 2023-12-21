use std::iter;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Find the roots of a quadratic expression ax^2 + bx + c.
fn roots(a: f64, b: f64, c: f64) -> (f64, f64) {
    let sqrt_term = (b.powi(2) - 4_f64 * a * c).sqrt();
    let rs = ((-b - sqrt_term) / (2_f64 * a), (-b + sqrt_term) / (2_f64 * a));
    if rs.0 <= rs.1 {
        return rs;
    } else {
        return (rs.1, rs.0);
    }
}

fn solution_p1(input: String) -> usize {

    let mut lines = input.lines();

    let times = lines.next().expect("Should have times line.")
        .split(':').last().expect("Should have colon delimiter.")
        .split(' ')
        .filter(|s| *s != "")
        .map(|s| s.parse::<usize>().expect("Should have valid times."));

    let distances = lines.next().expect("Should have distances line.")
        .split(':').last().expect("Should have colon delimiter.")
        .split(' ')
        .filter(|s| *s != "")
        .map(|s| s.parse::<usize>().expect("Should have valid distances."));

    iter::zip(times, distances)
        .map(|(t, d)| {
            let r = roots(-1_f64, t as f64, - (d as f64) - 1_f64);
            (r.1.floor() - r.0.ceil()) as usize + 1
        })
        .reduce(|acc, n| acc * n)
        .expect("Must have at least one race.")

}

fn solution_p2(input: String) -> usize {

    let mut lines = input.lines();

    let times_str = lines.next().expect("Should have times line.")
        .split(':').last().expect("Should have colon delimiter.");
    let time = String::from(times_str)
        .replace(" ", "")
        .parse::<usize>()
        .expect("Should have valid times.");

    let times_str = lines.next().expect("Should have distances line.")
        .split(':').last().expect("Should have colon delimiter.");
    let dist = String::from(times_str)
        .replace(" ", "")
        .parse::<usize>()
        .expect("Should have valid distances.");

   let r = roots(-1_f64, time as f64, - (dist as f64) - 1_f64);
   (r.1.floor() - r.0.ceil()) as usize + 1

}


#[cfg(test)]
mod tests {
    use crate::day6::{solution_p1, solution_p2};

    const EXAMPLE: &str = "Time:      7  15   30\nDistance:  9  40  200\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 288);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 71503);
    }
}
