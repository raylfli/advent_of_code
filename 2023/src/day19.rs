use std::collections::HashMap;

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Parse rule into representative tuple.
/// 
/// Returned tuple is of the form (op, var, value, label). Where op is:
///     * 0 for no rule
///     * 1 for less than
///     * 2 for greater than
fn parse_rule(rule: &str) -> (u8, char, u64, &str) {

    if rule.contains(':') {
        let (rule_expr, label) = rule.split(':').collect_tuple().expect("Must have a rule and a label.");
        let op = if rule_expr.contains('<') { 1_u8 } else { 2_u8 };

        let (var, value) = rule_expr
            .split(if op == 1_u8 { '<' } else { '>' })
            .collect_tuple()
            .unwrap();
        let var = var.chars().next().expect("Rule must have a variable.");
        let value = value.parse::<u64>().expect("Rule must have valid number.");

        (op, var, value, label)
    } else {
        (0, 'x', 0, rule) // variable should be ignored
    }

}

/// Parse rules into representative tuples.
fn parse_rules(rule_str: &str) -> HashMap<&str, Vec<(u8, char, u64, &str)>> {

    rule_str
        .lines()
        .map(|line| {
            let (label, rules) = line.split("{").collect_tuple().expect("Rule must have label and rules.");
            let rules = (&rules[0..rules.len() - 1])
                .split(',')
                .map(|rule| parse_rule(rule))
                .collect_vec();
            (label, rules)
        })
        .collect::<HashMap<_, _>>()

}

/// Apply a rule to a part.
fn apply_rule<'a>(rules: &Vec<(u8, char, u64, &'a str)>, part: &[u64; 4]) -> &'a str {

    for rule in rules {
        let (op, var, value, label) = rule;
        let var = match var {
            'x' => 0,
            'm' => 1,
            'a' => 2,
            _ => 3,
        };
        if *op == 0_u8 {
            return label;
        }
        if *op == 1_u8 && part[var] < *value {
            return label;
        }
        if *op == 2_u8 && part[var] > *value {
            return label;
        }
    }

    ""

}

fn solution_p1(input: String) -> usize {

    let (rule_strs, part_strs) = input
        .split("\n\n")
        .collect_tuple()
        .expect("Must have rules and parts strings.");

    let rules = parse_rules(rule_strs);
    let parts = part_strs
        .lines()
        .map(|part_str| {
            let part_vars: (u64, u64, u64, u64) = (&part_str[1..part_str.len() - 1])
                .split(',')
                .map(|v| (&v[2..]).parse::<u64>().expect("Parts must have valid numeric value."))
                .collect_tuple()
                .expect("Must have four part variables.");

        [part_vars.0, part_vars.1, part_vars.2, part_vars.3]

        });

    let mut total = 0_u64;
    for part in parts {
        let mut label = "in";
        while label != "A" && label != "R" {
            let rule = rules.get(&label).expect("Must have matching rule.");
            label = apply_rule(rule, &part);
        }

        if label == "A" {
            total += part.into_iter().sum::<u64>();
        }
    }

    total as usize

}

fn solution_p2(input: String) -> u64 {

    let (rule_strs, _part_strs) = input
        .split("\n\n")
        .collect_tuple()
        .expect("Must have rules and parts strings.");

    let rules = parse_rules(rule_strs);

    // use intervals to figure out which intervals of XMAS values are accepted
    // intervals left endpoint inclusive: [a, b)
    type XmasRange = [(u64, u64); 4];

    // track which intervals are accepted
    let mut accepted: Vec<XmasRange> = vec![];

    // track which intervals need to be checked with a rule and subrule index
    let mut to_check: Vec<(&str, usize, XmasRange)> = vec![
        ("in", 0, [(1, 4001), (1, 4001), (1, 4001), (1, 4001)]),
    ];

    while to_check.len() > 0 {
        let (label, i, xmas) = to_check.pop().unwrap();
        
        // check if entire part is accepted
        if label == "A" {
            accepted.push(xmas);
            continue;
        }

        // if rejected, no need to continue
        if label == "R" {
            continue;
        }

        // otherwise, process with rules
        let (op, var, value, accept_label) = *rules
            .get(&label)
            .expect("Label must have matching rule")
            .get(i)
            .expect("Subrule index must be in bounds.");

        // no range check, automatically accepted by subrule
        if op == 0_u8 {
            to_check.push((
                accept_label,
                0,
                xmas,
            ));
            continue;
        }

        let xmas_i = match var {
            'x' => 0,
            'm' => 1,
            'a' => 2,
            _ => 3,
        };

        // check whether interval needs to be split
        let (xmas_l, xmas_r) = xmas[xmas_i];
        if xmas_l <= value && value < xmas_r {
            // split interval, partially accepted by subrule
            if op == 1_u8 {
                let mut new_xmas = xmas.clone();
                new_xmas[xmas_i] = (xmas_l, value);
                to_check.push((
                    accept_label,
                    0,
                    new_xmas
                ));
                let mut new_xmas = xmas.clone();
                new_xmas[xmas_i] = (value, xmas_r);
                to_check.push((
                    label,
                    i + 1,
                    new_xmas
                ));
            } else {
                let mut new_xmas = xmas.clone();
                new_xmas[xmas_i] = (xmas_l, value + 1);
                to_check.push((
                    label,
                    i + 1,
                    new_xmas
                ));
                let mut new_xmas = xmas.clone();
                new_xmas[xmas_i] = (value + 1, xmas_r);
                to_check.push((
                    accept_label,
                    0,
                    new_xmas
                ));
            }
        } else if (op == 2_u8 && value < xmas_l) || (op == 1_u8 && value >= xmas_r) {
            // entirely accepted by subrule
            to_check.push((
                accept_label,
                0,
                xmas,
            ));
        } else {
            // entirely rejected by subrule
            to_check.push((
                label,
                i + 1,
                xmas,
            ));
        }
    }

    accepted
        .into_iter()
        .map(|xmas| {
            xmas
                .into_iter()
                .map(|(l, r)| r - l)
                .fold(1_u64, |acc, n| acc * n)
        })
        .sum::<u64>()

}


#[cfg(test)]
mod tests {
    use crate::day19::{solution_p1, solution_p2};

    const EXAMPLE: &str = "px{a<2006:qkq,m>2090:A,rfg}\npv{a>1716:R,A}\nlnx{m>1548:A,A}\nrfg{s<537:gd,x>2440:R,A}\nqs{s>3448:A,lnx}\nqkq{x<1416:A,crn}\ncrn{x>2662:A,R}\nin{s<1351:px,qqz}\nqqz{s>2770:qs,m<1801:hdj,R}\ngd{a>3333:R,R}\nhdj{m>838:A,pv}\n\n{x=787,m=2655,a=1222,s=2876}\n{x=1679,m=44,a=2067,s=496}\n{x=2036,m=264,a=79,s=2244}\n{x=2461,m=1339,a=466,s=291}\n{x=2127,m=1623,a=2188,s=1013}\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 19114);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 167409079868000);
    }

}
