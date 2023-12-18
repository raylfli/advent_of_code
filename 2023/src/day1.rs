use std::cmp;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

fn solution_p1(input: String) -> u32 {
    let mut total: u32 = 0;
    for line in input.lines() {
        let mut s: String = String::from("");
        for c in line.chars() {
            if c.is_digit(10) {
                s.push(c);
            }
        }

        let n1 = s.chars()
            .next()
            .and_then(|c| c.to_digit(10))
            .expect("First numeric detected not a digit.");
        let n2 = s.chars()
            .last()
            .and_then(|c| c.to_digit(10))
            .expect("Second numeric detected not a digit.");
        total += n1 * 10 + n2;
    }
    return total;
}

fn solution_p2(input: String) -> u32 {
    let mut total: u32 = 0;
    for line in input.lines() {
        let mut s: String = String::from("");
        let line_chars: Vec<char> = line.to_string().chars().collect();
        for (i, c) in line_chars.iter().enumerate() {
            if c.is_digit(10) {
                s.push(*c);
            } else {
                let mut line_chars2 = line_chars.clone();
                line_chars2.push('*');
                line_chars2.push('*');
                match line_chars2[i..cmp::min(i+5, line_chars2.len())] {
                    ['o', 'n', 'e', _, _] => s.push('1'),
                    ['t', 'w', 'o', _, _] => s.push('2'),
                    ['t', 'h', 'r', 'e', 'e'] => s.push('3'),
                    ['f', 'o', 'u', 'r', _] => s.push('4'),
                    ['f', 'i', 'v', 'e', _] => s.push('5'),
                    ['s', 'i', 'x', _, _] => s.push('6'),
                    ['s', 'e', 'v', 'e', 'n'] => s.push('7'),
                    ['e', 'i', 'g', 'h', 't'] => s.push('8'),
                    ['n', 'i', 'n', 'e', _] => s.push('9'),
                    _ => (),
                }
            }
        }

        let n1 = s.chars()
            .next()
            .and_then(|c| c.to_digit(10))
            .expect("First numeric detected not a digit.");
        let n2 = s.chars()
            .last()
            .and_then(|c| c.to_digit(10))
            .expect("Second numeric detected not a digit.");
        total += n1 * 10 + n2;
    }
    return total;
}


#[cfg(test)]
mod tests {
    use crate::day1::{solution_p1, solution_p2};

    #[test]
    fn pt1() {
        let input = String::from("1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet\n");
        assert_eq!(solution_p1(input), 142);
    }

    #[test]
    fn pt2() {
        let input = String::from("two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen\n");
        assert_eq!(solution_p2(input), 281);
    }
}
