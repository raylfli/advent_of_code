use std::collections::HashSet;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Find the end indices of a number within a string from a start point.
/// 
/// Numbers will be searched for in b
/// 
/// End index is exclusive.
fn num_span(s: &Vec<char>, start: usize) -> &[char] {
    let mut i = start;

    while i < s.len() && s[i].is_digit(10) {
        i += 1
    }

    &s[(start as usize)..i]
}

/// Return whether there exists a symbol in the neighbours of a given cell.
/// 
/// Symbols are defined as non-numeric and non-period "." characters.
fn has_symbol(lines: &Vec<Vec<char>>, cell: (usize, usize)) -> bool {

    for di in -1..2 {
        for dj in -1..2 {
            let i = (cell.0 as isize) + di;
            let j = (cell.1 as isize) + dj;

            if 
                i >= 0 && 
                j >= 0 && 
                (i as usize) < lines.len() && 
                (j as usize) < lines.get(0).expect("At least one line should exist.").len() && 
                !lines[i as usize][j as usize].is_digit(10) && 
                lines[i as usize][j as usize] != '.' {
                    return true;
                }
        }
    }

    false
}

fn solution_p1(input: String) -> usize {
    let mut total: usize = 0;
    let lines: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();
    for (line_i, line) in lines.iter().enumerate() {

        let mut i = 0;
        while i < line.len() {
            if line[i].is_digit(10) {
                let char_slice = num_span(&line, i);

                'num_check: for check_i in i..(i + char_slice.len()) {
                    if has_symbol(&lines, (line_i, check_i)) {

                        total += char_slice.iter().collect::<String>().parse::<usize>().expect("Should add valid number.");
                        break 'num_check;
                    }
                }

                i += char_slice.len();
            } else {

                i += 1;

            }
        }
    }

    total

}

/// Return the end indices of a number at a given location.
/// 
/// Location can be any significance location, search will proceed left and right of the given location.
fn num_around(line: &Vec<char>, i: usize) -> Option<(usize, usize)> {
    let mut l = i as isize;
    let mut r = i as isize;

    if !line.get(i as usize).expect("Valid column.").is_digit(10) {
        return None;
    }

    // find left bound
    while l >= 0 && line[l as usize].is_digit(10) {
        l -= 1;
    }
    if l < i as isize {
        l += 1;
    }

    // find right bound
    while r < line.len() as isize && line[r as usize].is_digit(10) {
        r += 1;
    }
    if r > i as isize {
        r -= 1;
    }

    Some((l as usize, (r as usize) + 1))
}

/// Return the numbers around a given cell.
/// 
/// Symbols are defined as non-numeric and non-period "." characters.
fn nums_around(lines: &Vec<Vec<char>>, cell: (usize, usize)) -> Vec<usize> {

    let mut nums: HashSet<(usize, usize, usize)> = HashSet::new();

    for di in -1..2 {
        for dj in -1..2 {
            let i = (cell.0 as isize) + di;
            let j = (cell.1 as isize) + dj;

            if 
                i >= 0 && 
                j >= 0 && 
                (i as usize) < lines.len() && 
                (j as usize) < lines.get(0).expect("At least one line should exist.").len() {
                    let bounds = num_around(&lines[i as usize], j as usize);
                    match bounds {
                        Some((l, r)) => nums.insert((i as usize, l, r)),
                        _ => false,
                    };
                }
        }
    }

    nums
        .iter()
        .map(|(i, l, r)| lines[*i][*l..*r].iter()
            .collect::<String>()
            .parse::<usize>()
            .expect("Valid number."))
        .collect::<Vec<usize>>()
}

fn solution_p2(input: String) -> usize {
    let mut total: usize = 0;
    let lines: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();
    for (line_i, line) in lines.iter().enumerate() {

        let mut i = 0;
        while i < line.len() {
            if line[i] == '*' {
                let around = nums_around(&lines, (line_i, i));

                if around.len() == 2 {
                    total += around.iter().fold(1, |acc, n| acc * n);
                }

            }

            i += 1;

        }
    }

    total
}


#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use crate::day3::{solution_p1, solution_p2, num_span, num_around, nums_around};

    const EXAMPLE: &str = "467..114..\n...*......\n..35..633.\n......#...\n617*......\n.....+.58.\n..592.....\n......755.\n...$.*....\n.664.598..\n";

    #[test]
    fn span_start() {
        let input = String::from("467..114..").chars().collect::<Vec<char>>();
        assert_eq!(num_span(&input, 0), &input[0..3]);
    }

    #[test]
    fn span_middle() {
        let input = String::from("467..114..").chars().collect::<Vec<char>>();
        assert_eq!(num_span(&input, 5), &input[5..8]);
    }

    #[test]
    fn span_end() {
        let input = String::from("467..114").chars().collect::<Vec<char>>();
        assert_eq!(num_span(&input, 5), &input[5..8]);
    }

    #[test]
    fn num_around_begin() {
        let input = String::from("467..114").chars().collect::<Vec<char>>();
        assert_eq!(num_around(&input, 0), Some((0, 3)));
    }

    #[test]
    fn num_around_mid() {
        let input = String::from("467..114").chars().collect::<Vec<char>>();
        assert_eq!(num_around(&input, 1), Some((0, 3)));
    }
    
    #[test]
    fn num_around_end() {
        let input = String::from("467..114").chars().collect::<Vec<char>>();
        assert_eq!(num_around(&input, 2), Some((0, 3)));
    }
    
    #[test]
    fn nums_around_basic() {
        let input = vec![
            "467..114..".chars().collect::<Vec<char>>(),
            "...*......".chars().collect::<Vec<char>>(),
            "..35..633.".chars().collect::<Vec<char>>()];
        dbg!(input.clone());
        let exp: HashSet<usize> = HashSet::from([467, 35]);
        for n in nums_around(&input, (1, 3)) {
            match exp.get(&n) {
                Some(_) => assert!(true),
                _ => assert!(false),
            }
        }
    }

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 4361);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 467835);
    }
}
