use std::collections::HashMap;

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Output the current value from running the Holiday ASCII String Helper algorithm.
fn hash_algo(s: &str) -> usize {

    let mut cv = 0_usize;
    for c in s.chars() {
        cv += c as usize;
        cv *= 17;
        cv %= 256;
    }

    cv

}

fn solution_p1(input: String) -> usize {

    input
        .trim()
        .split(',')
        .map(|s| hash_algo(s))
        .sum()
    
}

fn solution_p2(input: String) -> usize {

    let mut box_allocations: HashMap<&str, (usize, usize)> = HashMap::new(); // label -> (box, index)
    const VEC_EMPTY: Vec<usize> = vec![]; // focal length
    let mut boxes = [VEC_EMPTY; 256];

    for s in input.trim().split(',') {
        let instr = s.split('=').collect_vec();
        match instr.len() {
            1 => {
                // remove from box
                let label = &instr[0][..instr[0].len() - 1];
                // let (corr_box, ind) = *(box_allocations.get(&label).expect("Must have been allocated."));
                match box_allocations.get(&label) {
                    Some((corr_box, ind)) => {
                        boxes[*corr_box][*ind] = 0;
                        box_allocations.remove(&label);
                    },
                    None => {}
                }
            },
            2 => {
                // add to box
                let label = instr[0];
                let focal_length = instr[1].parse::<usize>().expect("Must have valid focal length.");
                if box_allocations.contains_key(&label) {
                    let (corr_box, ind) = *(box_allocations.get(&label).expect("Must have been allocated."));
                    boxes[corr_box][ind] = focal_length;
                } else {
                    let corr_box = hash_algo(label);
                    let ind = boxes[corr_box].len();
                    boxes[corr_box].push(focal_length);
                    box_allocations.insert(&label, (corr_box, ind));
                }
            },
            _ => {}
        }
    }

    let mut total = 0_usize;
    for (box_i, contents) in boxes.into_iter().enumerate() {
        total += contents
            .into_iter()
            .filter(|foc_len| *foc_len > 0)
            .enumerate()
            .map(|(i, foc_len)| {
                (box_i + 1) * (i + 1) * foc_len
            })
            .sum::<usize>()
    }

    total

}


#[cfg(test)]
mod tests {
    use crate::day15::{solution_p1, solution_p2, hash_algo};

    const EXAMPLE: &str = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7\n";

    #[test]
    fn test_hash_1() {
        assert_eq!(hash_algo("rn=1"), 30);
    }

    #[test]
    fn test_hash_2() {
        assert_eq!(hash_algo("cm-"), 253);
    }

    #[test]
    fn test_hash_3() {
        assert_eq!(hash_algo("qp=3"), 97);
    }

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 1320);
    }
    

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 145);
    }

}
