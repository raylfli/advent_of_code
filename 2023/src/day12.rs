pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Solve one line for number of arrangements.
fn solve_line(line: &str, dup: usize) -> usize {
    
    let mut parts = line.split(' ');

    let spring_str = parts.next().expect("Must have spring conditions.");
    let mut spring_str_vec = vec![];
    for _ in 0..dup {
        spring_str_vec.push(spring_str);
    }
    let springs = (spring_str_vec.join("?") + ".")
        .chars()
        .collect::<Vec<_>>();
    
    let groups = parts.next().expect("Must have groupings.")
        .trim()
        .split(',')
        .map(|s| s.parse::<usize>().expect("Must have valid group numbers."))
        .collect::<Vec<_>>()
        .repeat(dup);

    let mut m = vec![vec![vec![0_usize; springs.len() + 2]; groups.len() + 2]; springs.len() + 1];
    m[0][0][0] = 1; // only one possible arrangement to begin
    for i in 0..springs.len() {
        for g in 0..groups.len() + 1 {
                for c in 0..springs.len() + 1 {
                    let spring = springs[i]; // current spring type
                    let arrs = m[i][g][c]; // current number of arrangements

                    if arrs == 0 {
                        continue;
                    }

                    if spring == '.' || spring == '?' {
                        // end group or noop
                        if c == 0 || c == groups[g - 1] {
                            m[i + 1][g][0] += arrs;
                        }
                    }

                    if spring == '#' || spring == '?' {
                        // start or continue group
                        m[i + 1][g + ((c == 0) as usize)][c + 1] += arrs;
                    }
                }
        }
    }

    m[springs.len()][groups.len()][0]

}

fn solution_p1(input: String) -> usize {

    input
        .lines()
        .map(|line| solve_line(line, 1))
        .sum()

}

fn solution_p2(input: String) -> usize {

    input
        .lines()
        .map(|line| solve_line(line, 5))
        .sum()

}


#[cfg(test)]
mod tests {
    use crate::day12::{solution_p1, solution_p2};

    const EXAMPLE: &str = "???.### 1,1,3\n.??..??...?##. 1,1,3\n?#?#?#?#?#?#?#? 1,3,1,6\n????.#...#... 4,1,1\n????.######..#####. 1,6,5\n?###???????? 3,2,1\n";

    #[test]
    fn test_solve_1() {
        let input = String::from("???.### 1,1,3\n");
        assert_eq!(solution_p1(input), 1);
    }

    #[test]
    fn test_solve_2() {
        let input = String::from(".??..??...?##. 1,1,3\n");
        assert_eq!(solution_p1(input), 4);
    }

    #[test]
    fn test_solve_3() {
        let input = String::from("?#?#?#?#?#?#?#? 1,3,1,6\n");
        assert_eq!(solution_p1(input), 1);
    }

    #[test]
    fn test_solve_4() {
        let input = String::from("????.#...#... 4,1,1\n");
        assert_eq!(solution_p1(input), 1);
    }

    #[test]
    fn test_solve_5() {
        let input = String::from("????.######..#####. 1,6,5\n");
        assert_eq!(solution_p1(input), 4);
    }

    #[test]
    fn test_solve_6() {
        let input = String::from("?###???????? 3,2,1\n");
        assert_eq!(solution_p1(input), 10);
    }

    #[test]
    fn test_solve_7() {
        let input = String::from("???.### 1,1,3\n");
        assert_eq!(solution_p2(input), 1);
    }

    #[test]
    fn test_solve_8() {
        let input = String::from(".??..??...?##. 1,1,3\n");
        assert_eq!(solution_p2(input), 16384);
    }

    #[test]
    fn test_solve_9() {
        let input = String::from("?#?#?#?#?#?#?#? 1,3,1,6\n");
        assert_eq!(solution_p2(input), 1);
    }

    #[test]
    fn test_solve_10() {
        let input = String::from("????.#...#... 4,1,1\n");
        assert_eq!(solution_p2(input), 16);
    }

    #[test]
    fn test_solve_11() {
        let input = String::from("????.######..#####. 1,6,5\n");
        assert_eq!(solution_p2(input), 2500);
    }

    #[test]
    fn test_solve_12() {
        let input = String::from("?###???????? 3,2,1\n");
        assert_eq!(solution_p2(input), 506250);
    }

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 21);
    }
    

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 525152);
    }

}
