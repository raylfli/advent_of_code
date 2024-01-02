use std::collections::{HashSet, VecDeque};

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Find location of start point.
fn find_start(map: &Vec<Vec<char>>) -> (usize, usize) {
    for (r, row) in map.iter().enumerate() {
        for (c, col) in row.iter().enumerate() {
            if *col == 'S' {
                return (r, c);
            }
        }
    }

    (0, 0)
}

/// Find distance to all tiles.
fn tile_distance(map: Vec<Vec<char>>) -> HashSet<(isize, isize, usize)> {
    let (start_r, start_c) = find_start(&map);

    let n_rows = map.len() as isize;
    let n_cols = map[0].len() as isize;

    // depth limited BFS to find furthest reachable plot
    let mut frontier: VecDeque<(isize, isize, usize)> = VecDeque::from([(start_r as isize, start_c as isize, 0)]);
    let mut reachable: HashSet<(isize, isize, usize)> = HashSet::new();
    let mut visited: HashSet<(isize, isize)> = HashSet::new();

    while frontier.len() > 0 {
        let (r, c, steps) = frontier.pop_front().unwrap();

        // if already visited, guaranteed to be greater steps since using BFS
        if visited.contains(&(r, c)) {
            continue;
        }
        visited.insert((r, c));
        reachable.insert((r, c, steps));

        // generate and expand neighbours
        for (dr, dc) in [
            (0_isize, 1_isize),
            (1_isize, 0_isize),
            (0_isize, -1_isize),
            (-1_isize, 0_isize),
        ] {
            let (new_r, new_c) = (r + dr, c + dc);
            if new_r >= 0 && new_r < n_rows &&
                new_c >= 0 && new_c < n_cols &&
                map[new_r as usize][new_c as usize] != '#' {
                    frontier.push_back((new_r, new_c, steps + 1));
            }
        }
    }

    reachable
}

/// Find number of reachable plots given a number of steps.
fn reachable_plots(map: Vec<Vec<char>>, steps_goal: usize) -> usize {

    let reachable = tile_distance(map);

    let steps_goal_parity = steps_goal % 2;
    reachable
        .into_iter()
        .filter(|(_r, _c, steps)| *steps <= steps_goal && *steps % 2 == steps_goal_parity)
        .count()

}

fn solution_p1(input: String) -> usize {

    let map = input
        .lines()
        .map(|line| {
            line
                .chars()
                .collect_vec()
        })
        .collect_vec();

    reachable_plots(map, 64)

}

/// Find number of reachable plots given a number of steps.
/// 
/// Uses input diamond and size assumptions.
fn reachable_plots_infinite(map: Vec<Vec<char>>, steps_goal: usize) -> usize {

    const MAP_SIZE: usize = 131;
    const MAP_SIZE_HALF: usize = MAP_SIZE / 2;

    let reachable = tile_distance(map);

    let n = (steps_goal - MAP_SIZE_HALF) / MAP_SIZE;
    let even = reachable.iter().filter(|(_r, _c, steps)| *steps % 2 == 0).count();
    let odd = reachable.iter().filter(|(_r, _c, steps)| *steps % 2 == 1).count();

    let even_corners = reachable.iter().filter(|(_r, _c, steps)| *steps > MAP_SIZE_HALF && *steps % 2 == 0).count();
    let odd_corners = reachable.iter().filter(|(_r, _c, steps)| *steps > MAP_SIZE_HALF && *steps % 2 == 1).count();

    (n + 1).pow(2) * odd + n.pow(2) * even - (n + 1) * odd_corners + n * even_corners

}

fn solution_p2(input: String) -> usize {

    let map = input
        .lines()
        .map(|line| {
            line
                .chars()
                .collect_vec()
        })
        .collect_vec();

    reachable_plots_infinite(map, 26501365)

}


#[cfg(test)]
mod tests {
    use itertools::Itertools;

    use crate::day21::reachable_plots;

    const EXAMPLE: &str = "...........\n.....###.#.\n.###.##..#.\n..#.#...#..\n....#.#....\n.##..S####.\n.##..#...#.\n.......##..\n.##.#.####.\n.##..##.##.\n...........\n";

    #[test]
    fn test_reachable_plots() {
        let input = String::from(EXAMPLE);
        let map = input.lines().map(|line| line.chars().collect_vec()).collect_vec();
        assert_eq!(reachable_plots(map, 6), 16);
    }

}
