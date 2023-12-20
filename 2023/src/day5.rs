use std::cmp;
use std::ops::Range;
use std::thread;

use itertools::Itertools;

use iset;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Generate interval map to query the next soil/fertilizer/water/light/temperature/humidity/location interval.
/// 
/// Interval values map from an interval to the root key and root value values.
fn generate_map(input: String) -> iset::IntervalMap<usize, (usize, usize)> {
    let mut lines = input.lines();
    lines.next();  // discard label line

    let mut map_elements: Vec<(Range<usize>, (usize, usize))> = vec![];
    for line in lines {
        let mut nums = line.split(' ').map(|s| s.trim().parse::<usize>().expect("Map values must be valid numbers."));

        let value_root = nums.next().expect("Must have value root.");
        let key = nums.next().expect("Must have map key.");
        let n = nums.next().expect("Must have number of interval elements;.");

        map_elements.push((key..key + n, (key, value_root)));
    }

    map_elements.into_iter().collect::<iset::IntervalMap<usize, (usize, usize)>>()
}

/// Lookup value in a single map.
/// 
/// If value is not found, the query is returned (per the problem description).
fn lookup(map: &iset::IntervalMap<usize, (usize, usize)>, query: usize) -> usize {
    let mut interval = (*map).overlap(query);
    match interval.next() {
        Some((_r, (k, v))) => *v + query - *k,
        _ => query
    }
}

fn solution_p1(input: String) -> usize {
    let mut map_groups = input.split("\n\n");

    // process initial seeds
    let seeds = map_groups.next().expect("Seeds should be in the first line.")
        .split(':').last().expect("Seeds line should have a colon.")
        .trim().split(' ')
        .map(|s| s.parse::<usize>().expect("Seeds must be valid numbers."));

    let maps = map_groups
        .map(|s| generate_map(String::from(s)))
        .collect::<Vec<iset::IntervalMap<usize, (usize, usize)>>>();

    let location = seeds
        .map(|seed| maps.iter().fold(seed, |acc, map| lookup(map, acc)))
        .reduce(|acc, n| cmp::min(acc, n))
        .expect("Has at least one location.");

    location
}

fn solution_p2(input: String) -> usize {

    let mut map_groups = input.split("\n\n");

    // process initial seeds
    let seed_chunks = map_groups.next().expect("Seeds should be in the first line.")
        .split(':').last().expect("Seeds line should have a colon.")
        .trim().split(' ')
        .map(|s| s.parse::<usize>().expect("Seeds must be valid numbers."))
        .chunks(2);
    
    let seed_intervals = seed_chunks.into_iter()
        .map(|chunk| chunk.collect_tuple().expect("Seed chunks must be non-empty."))
        .map(|(r1, r2)| r1..(r1 + r2));

    let maps = map_groups
        .map(|s| generate_map(String::from(s)))
        .collect::<Vec<iset::IntervalMap<usize, (usize, usize)>>>();

    
    thread::scope(|scope|
        {
            let mut children = vec![];
            for chunk in seed_intervals.into_iter() {
                children.push(scope.spawn(|| -> usize {
                        let location = chunk
                            .map(|seed| maps.iter().fold(seed, |acc, map| lookup(map, acc)))
                            .min()
                            .expect("Has at least one location.");
                    location
                }));
            }
            children
                .into_iter()
                .map(|handle| handle.join().expect("Thread should finish successfully."))
                .min()
                .expect("Must have at least one seed to check.")
        }
    )
}


#[cfg(test)]
mod tests {
    use std::ops::Range;

    use crate::day5::{solution_p1, solution_p2, generate_map, lookup};

    const EXAMPLE: &str = "seeds: 79 14 55 13\n\nseed-to-soil map:\n50 98 2\n52 50 48\n\nsoil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15\n\nfertilizer-to-water map:\n49 53 8\n0 11 42\n42 0 7\n57 7 4\n\nwater-to-light map:\n88 18 7\n18 25 70\n\nlight-to-temperature map:\n45 77 23\n81 45 19\n68 64 13\n\ntemperature-to-humidity map:\n0 69 1\n1 0 69\n\nhumidity-to-location map:\n60 56 37\n56 93 4\n";

    #[test]
    fn generate_map_simple() {
        let input = String::from("seed-to-soil map:\n50 98 2\n52 50 48\n");
        assert_eq!(
            generate_map(input).into_iter(..).collect::<Vec<(Range<usize>, (usize, usize))>>(),
            (iset::interval_map!{
                98..100 => (98, 50),
                50..98 =>(50, 52)
            }).into_iter(..).collect::<Vec<(Range<usize>, (usize, usize))>>()
        );
    }

    #[test]
    fn lookup_left_endpoint() {
        let map = iset::interval_map!{
            98..100 => (98, 50),
            50..98 =>(50, 52)
        };
        assert_eq!(lookup(&map, 98), 50);
    }

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 35);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 46);
    }
}
