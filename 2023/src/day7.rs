use std::cmp::Ordering;

use counter::Counter;
use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Camel Card Hand
struct CamelHand {
    cards_char: Vec<u8>,
    kind: u8,
    value: usize,
}

impl CamelHand {
    pub fn new(cards: &str, value: usize) -> Self {
        let cards_char = cards.chars()
            .map(|c| match c {
                'A' => 14,
                'K' => 13,
                'Q' => 12,
                'J' => 11,
                'T' => 10,
                '9' => 9,
                '8' => 8,
                '7' => 7,
                '6' => 6,
                '5' => 5,
                '4' => 4,
                '3' => 3,
                _ => 2,
            }).collect_vec();
        
        // derive hand type
        let card_counter = cards_char.iter().map(|n| *n).collect::<Counter<_>>();
        let unique = card_counter.len();
        let kind = match unique {
            1 => 7,  // five of a kind
            2 => {
                if card_counter.k_most_common_ordered(1)[0].1 == 4 {
                    6 // four of a kind
                } else {
                    5 // full house
                }
            },
            3 => {
                if card_counter.k_most_common_ordered(1)[0].1 == 3 {
                    4 // three of a kind
                } else {
                    3 // two pair
                }
            }
            4 => 2, // one pair
            _ => 1, // high card,
        };

        Self {
            cards_char: cards_char,
            kind: kind,
            value: value,
        }
    }
}

impl PartialEq for CamelHand {
    fn eq(&self, other: &Self) -> bool {
        self.kind == other.kind && self.cards_char == other.cards_char
    }
}

impl Eq for CamelHand {}

impl Ord for CamelHand {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.kind == other.kind {
            self.cards_char.cmp(&other.cards_char)
        } else {
            self.kind.cmp(&other.kind)
        }
    }
}

impl PartialOrd for CamelHand {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn solution_p1(input: String) -> usize {

    input.lines()
        .map(|line| {
            let mut line_iter = line.split(' ');
            let cards = line_iter.next().expect("Hand must have cards.");
            let value = line_iter.next().expect("Hand must have value.")
                .parse::<usize>().expect("Value must be numeric.");
            CamelHand::new(cards, value)
        })
        .sorted()
        .enumerate()
        .map(|(i, hand)| {
            (i + 1) * hand.value
        })
        .sum()

}


/// Camel Card Hand with Joker Rules
struct CamelHandJoker {
    cards_char: Vec<u8>,
    kind: u8,
    value: usize,
}

impl CamelHandJoker {
    pub fn new(cards: &str, value: usize) -> Self {
        let cards_char = cards.chars()
            .map(|c| match c {
                'A' => 14,
                'K' => 13,
                'Q' => 12,
                'T' => 10,
                '9' => 9,
                '8' => 8,
                '7' => 7,
                '6' => 6,
                '5' => 5,
                '4' => 4,
                '3' => 3,
                '2' => 2,
                _ => 1,
            }).collect_vec();
        
        // derive hand type
        let card_counter = cards_char.iter()
            .map(|n| *n)
            .collect::<Counter<_>>();
        let unique = card_counter.len();

        // regular rules
        let mut kind = match unique {
            1 => 7,  // five of a kind
            2 => {
                if card_counter.k_most_common_ordered(1)[0].1 == 4 {
                    6 // four of a kind
                } else {
                    5 // full house
                }
            },
            3 => {
                if card_counter.k_most_common_ordered(1)[0].1 == 3 {
                    4 // three of a kind
                } else {
                    3 // two pair
                }
            }
            4 => 2, // one pair
            _ => 1, // high card,
        };

        if card_counter.contains_key(&1) {
            // handle joker rules
            let jokers = *(card_counter.get(&1).expect("Joker must exist."));
            kind = match kind {
                7 | 6 | 5 => 7,  // 5OK | 4OK | FH => 5OK
                4 => 6, // 3OK => 4OK 
                3 => { // 2P => 4OK | FH
                    if jokers == 2 {
                        6 // 4OK, combine with other pair
                    } else {
                        5 // FH, add to either of the pairs
                    }
                },
                2 => 4, // 1P => 3OK, add to pair XXJ, or grab one more JJX
                _ => 2, // HC => 1P, combine with one other card
            }
        }

        Self {
            cards_char: cards_char,
            kind: kind,
            value: value,
        }
    }
}

impl PartialEq for CamelHandJoker {
    fn eq(&self, other: &Self) -> bool {
        self.kind == other.kind && self.cards_char == other.cards_char
    }
}

impl Eq for CamelHandJoker {}

impl Ord for CamelHandJoker {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.kind == other.kind {
            self.cards_char.cmp(&other.cards_char)
        } else {
            self.kind.cmp(&other.kind)
        }
    }
}

impl PartialOrd for CamelHandJoker {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn solution_p2(input: String) -> usize {
    
    input.lines()
        .map(|line| {
            let mut line_iter = line.split(' ');
            let cards = line_iter.next().expect("Hand must have cards.");
            let value = line_iter.next().expect("Hand must have value.")
                .parse::<usize>().expect("Value must be numeric.");
            CamelHandJoker::new(cards, value)
        })
        .sorted()
        .enumerate()
        .map(|(i, hand)| {
            (i + 1) * hand.value
        })
        .sum()

}


#[cfg(test)]
mod tests {
    use crate::day7::{solution_p1, solution_p2};

    const EXAMPLE: &str = "32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 6440);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 5905);
    }
}
