use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Compute area given directions
fn area(directions: Vec<(char, usize)>) -> usize{

    let mut r = 0_f64;
    let mut c = 0_f64;
    
    let mut points: Vec<(f64, f64)> = vec![(r, c)];
    let mut n_points = 0_usize;

    for (direction, steps) in directions.into_iter() {
        let (dr, dc) = match direction {
            'U' => (-1_f64, 0_f64),
            'D' => (1_f64, 0_f64),
            'L' => (0_f64, -1_f64),
            _ => (0_f64, 1_f64),
        };
        r += dr * (steps as f64);
        c += dc * (steps as f64);
        points.push((r, c));
        n_points += steps;
    }

    let min_r = points.iter().map(|(r, _c)| *r).reduce(|acc, f| acc.min(f)).expect("Must have at least one point.");
    let min_c = points.iter().map(|(_r, c)| *c).reduce(|acc, f| acc.min(f)).expect("Must have at least one point.");

    points = points.into_iter().map(|(r, c)| (min_r + r, min_c + c)).collect_vec();

    let first = points[0];
    let last = points[points.len() - 1];

    // Shoelace formula for area
    let area = points
        .into_iter()
        .tuple_windows()
        .map(|((pr, pc), (qr, qc))| {
            (pr - qr) * (pc + qc)
        })
        .sum::<f64>();

    let last_edge = (last.0 - first.0) * (last.1 + first.1);

    let area = (area + last_edge).abs() / 2_f64;

    // Pick's algorithm for interior + boundary points
    ((area - (n_points as f64) / 2_f64 + 1_f64) + n_points as f64) as usize

}

fn solution_p1(input: String) -> usize {

    let directions = input
        .lines()
        .map(|line| {
            let split = line
                .split(' ')
                .collect_vec();
            (
                split[0].chars().next().expect("Must have at least one direction."),
                split[1].parse::<usize>().expect("Must have valid number of tiles."),
            )
        })
        .collect_vec();

    area(directions)

}

fn solution_p2(input: String) -> usize {

    let directions = input
        .lines()
        .map(|line| {
            let split = line
                .split(' ')
                .collect_vec();
            (
                match (&split[2][7..8]).chars().next().expect("Must have at least one direction.") {
                    '0' => 'R',
                    '1' => 'D',
                    '2' => 'L',
                    _ => 'U',
                },
                usize::from_str_radix(&split[2][2..7], 16).expect("Must be valid hex string."),
            )
        })
        .collect_vec();

    area(directions)

}


#[cfg(test)]
mod tests {
    use crate::day18::{solution_p1, solution_p2};

    const EXAMPLE: &str = "R 6 (#70c710)\nD 5 (#0dc571)\nL 2 (#5713f0)\nD 2 (#d2c081)\nR 2 (#59c680)\nD 2 (#411b91)\nL 5 (#8ceee2)\nU 2 (#caa173)\nL 1 (#1b58a2)\nU 2 (#caa171)\nR 2 (#7807d2)\nU 3 (#a77fa3)\nL 2 (#015232)\nU 2 (#7a21e3)\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 62);
    }
    

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 952408144115);
    }

}
