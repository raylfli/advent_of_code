use std::collections::HashSet;

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Check for a mirror between column `col1` and `col2`.
/// 
/// Returns 0, 1, or 2. 0 indicates a perfect mirror, 1 indicates a single mismatch, 2 indicates more than 1 mismatch.
fn check_col(pattern: &Vec<Vec<char>>, col1: usize, col2: usize) -> usize {
    let mut mismatches = 0_usize;
    for row in pattern.iter() {
        if row[col1] != row[col2] {
            mismatches += 1;
        }

        if mismatches > 1 {
            return 2;
        }
    }
    mismatches
}

/// Check for a mirror of reflection between rows `row1` and `row2`.
/// 
/// Returns 0, 1, or 2. 0 indicates a perfect mirror, 1 indicates a single mismatch, 2 indicates more than 1 mismatch.
fn check_row(pattern: &Vec<Vec<char>>, row1: usize, row2: usize) -> usize {
    let mut mismatches = 0;
    for (c1, c2) in pattern[row1].iter().zip(pattern[row2].iter()) {
        if c1 != c2 {
            mismatches += 1;
        }

        if mismatches > 1 {
            return 2;
        }
    }
    mismatches
}

/// Find the line of reflection for the pattern.
fn find_lor_col(pattern: &Vec<Vec<char>>, required_mismatches: usize) -> Option<usize> {

    let cols = pattern[0].len();
    let mut possible = (0..(cols - 1) as isize).collect::<HashSet<_>>();
    let mut changed = true;
    let mut total_mismatches;

    while changed && possible.len() > 0 {
        changed = false;
        total_mismatches = 0_usize;
        let check = *(possible.iter().next().expect("Must have at least one possibility."));
        for dilation in 0..(cols / 2) as isize {
            let c1 = check - dilation;
            let c2 = check + dilation + 1;
            if c1 >= 0 && (c2 as usize) < cols {
                total_mismatches += check_col(pattern, c1 as usize, c2 as usize);
                if total_mismatches > required_mismatches {
                    possible.remove(&check);
                    changed = true;
                    break;
                }
            }
        }

        if total_mismatches != required_mismatches {
            possible.remove(&check);
            changed = true;
        }
    }

    possible.into_iter().map(|n| n as usize).next()

}

/// Find the line of reflection for the pattern.
fn find_lor_row(pattern: &Vec<Vec<char>>, required_mismatches: usize) -> Option<usize> {

    let rows = pattern.len();
    let mut possible = (0..(rows - 1) as isize).collect::<HashSet<_>>();
    let mut changed = true;
    let mut total_mismatches;

    while changed && possible.len() > 0 {
        changed = false;
        total_mismatches = 0_usize;
        let check = *(possible.iter().next().expect("Must have at least one possibility."));
        for dilation in 0..(rows / 2) as isize {
            let r1 = check - dilation;
            let r2 = check + dilation + 1;
            if r1 >= 0 && (r2 as usize) < rows {
                total_mismatches += check_row(pattern, r1 as usize, r2 as usize);
                if total_mismatches > required_mismatches {
                    possible.remove(&check);
                    changed = true;
                    break;
                }
            }
        }

        if total_mismatches != required_mismatches {
            possible.remove(&check);
            changed = true;
        }
    }

    possible.into_iter().map(|n| n as usize).next()

}

fn solution_p1(input: String) -> usize {

    let mut total = 0_usize;

    for block in input.split("\n\n") {
        let mut rows = vec![];
        for line in block.lines() {
            rows.push(line.chars().collect_vec());
        }

        let poss_col = find_lor_col(&rows, 0);
        let poss_row = find_lor_row(&rows, 0);

        if let Some(col) = poss_col {
            total += col + 1;
        } else if let Some(row) = poss_row {
            total += 100_usize * (row + 1);
        } else {
            panic!("Patterns must have a line of reflection!");
        }
    }

    total

}

fn solution_p2(input: String) -> usize {

    let mut total = 0_usize;

    for block in input.split("\n\n") {
        let mut rows = vec![];
        for line in block.lines() {
            rows.push(line.chars().collect_vec());
        }

        let poss_col = find_lor_col(&rows, 1);
        let poss_row = find_lor_row(&rows, 1);

        if let Some(col) = poss_col {
            total += col + 1;
        } else if let Some(row) = poss_row {
            total += 100_usize * (row + 1);
        } else {
            panic!("Patterns must have a line of reflection!");
        }
    }

    total

}


#[cfg(test)]
mod tests {
    use crate::day13::{solution_p1, solution_p2, check_col, check_row, find_lor_col, find_lor_row};

    const EXAMPLE: &str = "#.##..##.\n..#.##.#.\n##......#\n##......#\n..#.##.#.\n..##..##.\n#.#.##.#.\n\n#...##..#\n#....#..#\n..##..###\n#####.##.\n#####.##.\n..##..###\n#....#..#\n";

    #[test]
    fn test_check_col_t_1() {
        let pattern = vec![vec!['#', '#']];
        assert_eq!(check_col(&pattern, 0, 1), 0);
    }

    #[test]
    fn test_check_col_t_2() {
        let pattern = vec![vec!['#', '.', '#']];
        assert_eq!(check_col(&pattern, 0, 2), 0);
    }

    #[test]
    fn test_check_col_f_1() {
        let pattern = vec![vec!['#', '.']];
        assert_eq!(check_col(&pattern, 0, 1), 1);
    }

    #[test]
    fn test_check_col_f_2() {
        let pattern = vec![vec!['#', '.', '.']];
        assert_eq!(check_col(&pattern, 0, 2), 1);
    }

    #[test]
    fn test_check_row_t() {
        let pattern = vec![vec!['#'], vec!['#']];
        assert_eq!(check_row(&pattern, 0, 1), 0);
    }

    #[test]
    fn test_check_row_f() {
        let pattern = vec![vec!['#'], vec!['.']];
        assert_eq!(check_row(&pattern, 0, 1), 1);
    }

    #[test]
    fn test_find_lor_col_t() {
        let pattern = vec![vec!['#', '#']];
        assert_eq!(find_lor_col(&pattern, 0), Some(0));
    }

    #[test]
    fn test_find_lor_col_f() {
        let pattern = vec![vec!['#', '.', '#']];
        assert_eq!(find_lor_col(&pattern, 0), None);
    }

    #[test]
    fn test_find_lor_row_t() {
        let pattern = vec![vec!['#'], vec!['#']];
        assert_eq!(find_lor_row(&pattern, 0), Some(0));
    }

    #[test]
    fn test_find_lor_row_f() {
        let pattern = vec![vec!['#'], vec!['.'], vec!['#']];
        assert_eq!(find_lor_row(&pattern, 0), None);
    }

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 405);
    }
    

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 400);
    }

}
