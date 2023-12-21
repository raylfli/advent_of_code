use std::collections::HashMap;
use num::integer::lcm;

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

fn solution_p1(input: String) -> usize {

    let mut lines = input.split("\n\n");

    let instructions = lines.next().expect("Must have directions line.").trim();
    let connections = lines.next().expect("Must have connections.")
        .trim()
        .split('\n')
        .map(|line| {
            let mut from_to = line.split(" = ");
            let from = from_to.next().expect("Must have 'from' label.");
            let to_str = from_to.next().expect("Must have 'to' tuple.");
            let to = to_str[1..to_str.len() - 1]
                .split(", ")
                .collect_tuple()
                .expect("Must have left and right branch.");
            (from, to)
        }).collect::<HashMap<&str, (&str, &str)>>();

    let mut node = "AAA";
    let mut steps = 0_usize;
    'loop_instr: while node != "ZZZ" {
        for instr in instructions.chars() {
            if instr == 'R' {
                node = connections[node].1;
            } else {
                node = connections[node].0;
            }
            steps += 1;

            if node == "ZZZ" {
                break 'loop_instr;
            }
        }
    }

    steps

}

fn solution_p2(input: String) -> usize {

    let mut lines = input.split("\n\n");

    let instructions = lines.next().expect("Must have directions line.").trim();
    let connections = lines.next().expect("Must have connections.")
        .trim()
        .split('\n')
        .map(|line| {
            let mut from_to = line.split(" = ");
            let from = from_to.next().expect("Must have 'from' label.");
            let to_str = from_to.next().expect("Must have 'to' tuple.");
            let to = to_str[1..to_str.len() - 1]
                .split(", ")
                .collect_tuple()
                .expect("Must have left and right branch.");
            (from, to)
        }).collect::<HashMap<&str, (&str, &str)>>();

    let nodes = connections.keys()
        .filter(|&k| (*k).ends_with('A'))
        .map(|s| *s)
        .collect_vec();

    // for each node, traverse until hitting __Z to find cycle length, then compute LCM of all starting nodes
    
    let cycle_lengths = nodes
        .into_iter()
        .map(|mut node| {
            let mut steps = 0_usize;
            'loop_instr: while !node.ends_with('Z') {
                for instr in instructions.chars() {
                    if instr == 'R' {
                        node = connections[node].1;
                    } else {
                        node = connections[node].0;
                    }
                    steps += 1;

                    if node.ends_with('Z') {
                        break 'loop_instr;
                    }
                }
            }

            steps
        });

    cycle_lengths.reduce(|acc, n| lcm(acc, n)).expect("Must have at least one cycle.")

}


#[cfg(test)]
mod tests {
    use crate::day8::{solution_p1, solution_p2};

    const EXAMPLE: &str = "RL\n\nAAA = (BBB, CCC)\nBBB = (DDD, EEE)\nCCC = (ZZZ, GGG)\nDDD = (DDD, DDD)\nEEE = (EEE, EEE)\nGGG = (GGG, GGG)\nZZZ = (ZZZ, ZZZ)\n";
    const EXAMPLE2: &str = "LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)\n";

    const EXAMPLE3: &str = "LR\n\n11A = (11B, XXX)\n11B = (XXX, 11Z)\n11Z = (11B, XXX)\n22A = (22B, XXX)\n22B = (22C, 22C)\n22C = (22Z, 22Z)\n22Z = (22B, 22B)\nXXX = (XXX, XXX)\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 2);
    }
    
    #[test]
    fn pt1_2() {
        let input = String::from(EXAMPLE2);
        assert_eq!(solution_p1(input), 6);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE3);
        assert_eq!(solution_p2(input), 6);
    }
}
