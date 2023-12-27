use std::collections::HashSet;

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Find number of energized tiles.
fn energized_tiles(cave: &Vec<Vec<char>>, start: (isize, isize, isize, isize)) -> usize {

    let rows = cave.len() as isize;
    let cols = cave[0].len() as isize;

    let mut to_check: Vec<(isize, isize, isize, isize)> = vec![start]; // (r, c, dr, dc)
    let mut split_checked: HashSet<(isize, isize, isize, isize)> = HashSet::new(); // (r, c, dr, dc)
    let mut energized: HashSet<(isize, isize)> = HashSet::new();

    while to_check.len() > 0 {
        let mut r;
        let mut c;
        let mut dr;
        let mut dc;
        (r, c, dr, dc) = to_check.pop().unwrap();

        if split_checked.contains(&(r, c, dr, dc)) {
            continue; // no need to recheck, in a cycle
        }
        split_checked.insert((r, c, dr, dc));

        // trace this beam until hits edge of cave
        'trace_beam: while r >= 0 && r < rows && c >= 0 && c < cols {
            energized.insert((r, c));

            // figure out what type of tile
            match cave[r as usize][c as usize] {
                '/' => {
                    (dr, dc) = (-dc, -dr);
                },
                '\\' => {
                    (dr, dc) = (dc, dr);
                },
                '|' => {
                    if dc != 0 {
                        to_check.push((r - 1, c, -1, 0));
                        to_check.push((r + 1, c, 1, 0));
                        break 'trace_beam;
                    }
                },
                '-' => {
                    if dr != 0 {
                        to_check.push((r, c - 1, 0, -1));
                        to_check.push((r, c + 1, 0, 1));
                        break 'trace_beam;
                    }
                },
                _ => {},
            }
            r += dr;
            c += dc;
        }
    }

    energized.len()

}

fn solution_p1(input: String) -> usize {

    let cave = input
        .lines()
        .map(|line| {
            line
                .chars()
                .collect_vec()
        })
        .collect_vec();

    energized_tiles(&cave, (0, 0, 0, 1))

}

fn solution_p2(input: String) -> usize {

    let cave = input
        .lines()
        .map(|line| {
            line
                .chars()
                .collect_vec()
        })
        .collect_vec();

    let rows = cave.len();
    let cols = cave[0].len();

    let mut to_check: Vec<(isize, isize, isize, isize)> = Vec::with_capacity(2 * (rows + cols));
    for r in 0..rows {
        to_check.push((r as isize, 0, 0, 1));
        to_check.push((r as isize, cols as isize - 1, 0, -1));
    }
    for c in 0..cols {
        to_check.push((0, c as isize, 1, 0));
        to_check.push((rows as isize - 1, c as isize, -1, 0));
    }

    to_check
        .into_iter()
        .map(|start| energized_tiles(&cave, start))
        .max()
        .expect("Must have at least one check tile.")

}


#[cfg(test)]
mod tests {
    use crate::day16::{solution_p1, solution_p2};

    const EXAMPLE: &str = r".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 46);
    }
    

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 51);
    }

}
