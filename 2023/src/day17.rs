use std::cmp::Reverse;
use std::collections::{HashSet, BinaryHeap};

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

fn solution_p1(input: String) -> usize {

    let blocks = input
        .lines()
        .map(|line| {
            line
                .chars()
                .map(|c| c.to_digit(10).expect("Must be digit heat loss.") as usize)
                .collect_vec()
        })
        .collect_vec();

    let n_rows = blocks.len();
    let n_cols = blocks[0].len();
    let max_mr = 3_isize;
    let max_mc = 3_isize;

    let mut frontier: BinaryHeap<Reverse<(usize, isize, isize, isize, isize)>> = BinaryHeap::new(); // (loss, r, c, mr, mc)
    let mut visited: HashSet<(isize, isize, isize, isize)> = HashSet::new(); // (r, c, mr, mc)

    frontier.push(Reverse((0, 0, 0, 0, 0)));

    while frontier.len() > 0 {
        let Reverse((loss, r, c, mr, mc)) = frontier.pop().unwrap();

        // if goal is reached, we're done
        if (r as usize, c as usize) == (n_rows - 1, n_cols - 1) {
            return loss;
        }
        
        if !visited.contains(&(r, c, mr, mc)) {
            visited.insert((r, c, mr, mc));

            // generate and add neighbours to frontier
            for (dr, dc) in [
                    (0_isize, 1_isize),
                    (1_isize, 0_isize),
                    (0_isize, -1_isize),
                    (-1_isize, 0_isize),
                ] {
                let new_r = r + dr;
                let new_c = c + dc;
                let mr_dir_match = mr.signum() * dr.signum(); // == 1 when same direction
                let mc_dir_match = mc.signum() * dc.signum(); // == -1 or 0 when opposite direction or no movement

                // check if valid neighbour
                if new_r >= 0 && new_r < n_rows as isize && new_c >= 0 && new_c < n_cols as isize {
                    if (mr_dir_match == 1 && mr + dr > max_mr) || (mc_dir_match == 1 && mc + dc > max_mc) {
                        // invalid neighbour: momentum too high
                        continue;
                    }
                    if mr_dir_match == -1 || mc_dir_match == -1 {
                        // invalid neighbour: going reverse direction
                        continue;
                    }

                    // add new node to frontier
                    let new_mr = if mr_dir_match == 1 { mr + dr } else { dr };
                    let new_mc = if mc_dir_match == 1 { mc + dc } else { dc };
                    frontier.push(Reverse((
                        loss + blocks[new_r as usize][new_c as usize],
                        new_r,
                        new_c,
                        new_mr,
                        new_mc,
                    )));
                }

            }
        }
    }

    0

}

fn solution_p2(input: String) -> usize {

    let blocks = input
        .lines()
        .map(|line| {
            line
                .chars()
                .map(|c| c.to_digit(10).expect("Must be digit heat loss.") as usize)
                .collect_vec()
        })
        .collect_vec();

    let n_rows = blocks.len();
    let n_cols = blocks[0].len();
    let min_mr = 4_isize;
    let min_mc = 4_isize;
    let max_mr = 10_isize;
    let max_mc = 10_isize;

    let mut frontier: BinaryHeap<Reverse<(usize, isize, isize, isize, isize)>> = BinaryHeap::new(); // (loss, r, c, mr, mc)
    let mut visited: HashSet<(isize, isize, isize, isize)> = HashSet::new(); // (r, c, mr, mc)

    frontier.push(Reverse((blocks[0][1], 0, 1, 0, 1)));
    frontier.push(Reverse((blocks[1][0], 1, 0, 1, 0)));

    while frontier.len() > 0 {
        let Reverse((loss, r, c, mr, mc)) = frontier.pop().unwrap();

        // if goal is reached with correct momentum, we're done
        if (r as usize, c as usize) == (n_rows - 1, n_cols - 1) && (mr >= min_mr || mc >= min_mc) {
            return loss;
        }
        
        if !visited.contains(&(r, c, mr, mc)) {
            visited.insert((r, c, mr, mc));

            // must keep going straight if momentum isn't high enough
            if mr.abs() < min_mr && mc.abs() < min_mc {
                let new_r = r + mr.signum();
                let new_c = c + mc.signum();
                let new_mr = mr + mr.signum();
                let new_mc = mc + mc.signum();
                if new_r >= 0 && new_r < n_rows as isize && new_c >= 0 && new_c < n_cols as isize {
                    frontier.push(Reverse((
                        loss + blocks[new_r as usize][new_c as usize],
                        new_r,
                        new_c,
                        new_mr,
                        new_mc,
                    )));
                }
                continue;
            }

            // generate and add neighbours to frontier
            for (dr, dc) in [
                    (0_isize, 1_isize),
                    (1_isize, 0_isize),
                    (0_isize, -1_isize),
                    (-1_isize, 0_isize),
                ] {
                let new_r = r + dr;
                let new_c = c + dc;
                let mr_dir_match = mr.signum() * dr.signum(); // == 1 when same direction
                let mc_dir_match = mc.signum() * dc.signum(); // == -1 or 0 when opposite direction or no movement

                // check if valid neighbour
                if new_r >= 0 && new_r < n_rows as isize && new_c >= 0 && new_c < n_cols as isize {
                    if (mr_dir_match == 1 && (mr + dr).abs() > max_mr) || (mc_dir_match == 1 && (mc + dc).abs() > max_mc) {
                        // invalid neighbour: momentum too high
                        continue;
                    }
                    if mr_dir_match == -1 || mc_dir_match == -1 {
                        // invalid neighbour: going reverse direction
                        continue;
                    }

                    // add new node to frontier
                    let new_mr = if mr_dir_match == 1 { mr + dr } else { dr };
                    let new_mc = if mc_dir_match == 1 { mc + dc } else { dc };
                    frontier.push(Reverse((
                        loss + blocks[new_r as usize][new_c as usize],
                        new_r,
                        new_c,
                        new_mr,
                        new_mc,
                    )));
                }

            }
        }
    }

    0

}


#[cfg(test)]
mod tests {
    use crate::day17::{solution_p1, solution_p2};

    const EXAMPLE: &str = "2413432311323\n3215453535623\n3255245654254\n3446585845452\n4546657867536\n1438598798454\n4457876987766\n3637877979653\n4654967986887\n4564679986453\n1224686865563\n2546548887735\n4322674655533\n";
    const EXAMPLE2: &str = "111111111111\n999999999991\n999999999991\n999999999991\n999999999991\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 102);
    }
    

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 94);
    }

    #[test]
    fn pt2_2() {
        let input = String::from(EXAMPLE2);
        assert_eq!(solution_p2(input), 71);
    }

}
