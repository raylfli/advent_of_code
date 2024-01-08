use itertools::Itertools;
use nalgebra::{Matrix6, Vector6};

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Compute path itersections within provided test area
/// 
/// Considers only the x and y axes
fn path_intersections_2d(input: String, test_x: (f64, f64), test_y: (f64, f64)) -> usize {

    let paths = input
        .lines()
        .map(|line| {
            let mut coords = line.split('@');
            let p: (f64, f64, f64) = coords
                .next().expect("Must have path root.")
                .split(',')
                .map(|c| c.trim().parse::<i64>().expect("Must be valid coordinate (p).") as f64)
                .collect_tuple()
                .expect("Must have coordinate of dimension 3.");
            let d: (f64, f64, f64) = coords
                .next().expect("Must have path direction.")
                .split(',')
                .map(|c| c.trim().parse::<i64>().expect("Must be valid coordinate (d).") as f64)
                .collect_tuple()
                .expect("Must have coordinate of dimension 3.");

            (p, d)
        })
        .collect_vec();

    let mut count = 0_usize;
    for combo in paths.iter().combinations(2) {
        let (p1, d1) = combo[0];
        let (p2, d2) = combo[1];

        // solve using Cramer's rule (https://en.wikipedia.org/wiki/Cramer%27s_rule)

        let denom = d1.0 * (-d2.1) - (-d2.0) * d1.1;
        if denom.abs() > 0.00000000001_f64 {
            // far enough away from 0
            let p = (p2.0 - p1.0, p2.1 - p1.1);
            let t1 = (p.0 * (-d2.1) - (-d2.0) * p.1) / denom;
            let t2 = (d1.0 * p.1 - p.0 * d1.1) / denom;
            if t1 >= 0_f64 && t2 >= 0_f64 {
                // both stones collide in future
                let col_p1 = (t1 * d1.0 + p1.0, t1 * d1.1 + p1.1);
                // let col_p2 = (t2 * d2.0 + p2.0, t2 * d2.1 + p2.1); // should equal col_pq

                // check test zone collision boundary
                if col_p1.0 >= test_x.0 && col_p1.0 <= test_x.1 && col_p1.1 >= test_y.0 && col_p1.1 <= test_y.1 {
                    count += 1;
                }
            }
        }
    }

    count

}

fn solution_p1(input: String) -> usize {

    path_intersections_2d(input, (200000000000000_f64, 400000000000000_f64), (200000000000000_f64, 400000000000000_f64))

}

fn solution_p2(input: String) -> usize {

    let stones = input
        .lines()
        .map(|line| {
            let mut coords = line.split('@');
            let p: Vec<f64> = coords
                .next().expect("Must have path root.")
                .split(',')
                .map(|c| c.trim().parse::<i64>().expect("Must be valid coordinate (p).") as f64)
                .collect_vec();
            let d: Vec<f64> = coords
                .next().expect("Must have path direction.")
                .split(',')
                .map(|c| c.trim().parse::<i64>().expect("Must be valid coordinate (d).") as f64)
                .collect_vec();

            (p, d)
        })
        .collect_vec();

    // pairs for linear system in the format ((stone_i, stone_j), (axis_i, axis_j))
    const SYSTEM_PAIRS: [((usize, usize), (usize, usize)); 6] = [
        ((1, 2), (0, 1)),
        ((1, 2), (1, 2)),
        ((1, 2), (0, 2)),
        ((1, 3), (0, 1)),
        ((1, 3), (1, 2)),
        ((1, 3), (0, 2)),
    ];

    // for solving the system mx = b
    let mut m: Matrix6<f64> = Matrix6::zeros();
    let mut b: Vector6<f64> = Vector6::zeros();

    for (i, ((stone_i, stone_j), (axis_i, axis_j))) in SYSTEM_PAIRS.iter().enumerate() {
        let ((stone_i, stone_j), (axis_i, axis_j)) = ((*stone_i, *stone_j), (*axis_i, *axis_j));
        let mut row = m.row_mut(i);
        row[axis_i] = stones[stone_j].1[axis_j] - stones[stone_i].1[axis_j];
        row[axis_j] = stones[stone_i].1[axis_i] - stones[stone_j].1[axis_i];
        row[axis_i + 3] = stones[stone_i].0[axis_j] - stones[stone_j].0[axis_j];
        row[axis_j + 3] = stones[stone_j].0[axis_i] - stones[stone_i].0[axis_i];
        b[i] =
            stones[stone_j].0[axis_i] * stones[stone_j].1[axis_j] -
            stones[stone_j].0[axis_j] * stones[stone_j].1[axis_i] -
            stones[stone_i].0[axis_i] * stones[stone_i].1[axis_j] +
            stones[stone_i].0[axis_j] * stones[stone_i].1[axis_i];
    }

    let params = m.qr().solve(&b).expect("Should have solution.");

    (params[0] + params[1] + params[2]) as usize

}


#[cfg(test)]
mod tests {
    use crate::day24::{solution_p2, path_intersections_2d};

    const EXAMPLE: &str = "19, 13, 30 @ -2,  1, -2\n18, 19, 22 @ -1, -1, -2\n20, 25, 34 @ -2, -2, -4\n12, 31, 28 @ -1, -2, -1\n20, 19, 15 @  1, -5, -3\n";

    #[test]
    fn test_path_intersection() {
        let input = String::from(EXAMPLE);
        assert_eq!(path_intersections_2d(input, (7_f64, 27_f64), (7_f64, 27_f64)), 2);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 47);
    }

}
