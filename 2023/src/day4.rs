use std::cmp;
use std::collections::HashSet;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

fn solution_p1(input: String) -> usize {
    let mut total: usize = 0;

    for line in input.lines() {

        let card = line.split(":").last().expect("Card must include card ID.").trim();

        let mut num_groups = card.split("|");
        let winning = num_groups.next().expect("Card should have winning numbers.")
            .split(" ").filter(|n| *n != "").collect::<HashSet<&str>>();
        let nums = num_groups.last().expect("Card should have card check numbers.")
            .split(" ").filter(|n| *n != "").collect::<HashSet<&str>>();

        let matching = winning.intersection(&nums).count();
        if matching > 0 {
            total += (2 as usize).pow((matching - 1) as u32);
        }
    }

    total

}

fn solution_p2(input: String) -> usize {

    let mut copies: Vec<usize> = vec![1; input.lines().count()];

    for (i, line) in input.lines().enumerate() {

        let card = line.split(":").last().expect("Card must include card ID.").trim();

        let mut num_groups = card.split("|");
        let winning = num_groups.next().expect("Card should have winning numbers.")
            .split(" ").filter(|n| *n != "").collect::<HashSet<&str>>();
        let nums = num_groups.last().expect("Card should have card check numbers.")
            .split(" ").filter(|n| *n != "").collect::<HashSet<&str>>();

        let card_copies = copies[i];
        let matching = winning.intersection(&nums).count();
        for j in (i + 1)..cmp::min(i + matching + 1, copies.len()) {
            copies[j] += card_copies;
        }
    }

    copies.iter().fold(0 as usize, |acc, c| acc + *c)
}


#[cfg(test)]
mod tests {
    use crate::day4::{solution_p1, solution_p2};

    const EXAMPLE: &str = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\nCard 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\nCard 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\nCard 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\nCard 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\nCard 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 13);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 30);
    }
}
