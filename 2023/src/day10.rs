use std::collections::{HashMap, HashSet};

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Return whether the check cell (row, column) is a valid INDEX within grid bounds.
fn check_bounds(rows: usize, cols: usize, check: (isize, isize)) -> bool {
    let (r, c) = check;
    r >= 0 && r < (rows as isize) && c >= 0 && c < (cols as isize)
}

/// Generate graph of pipe connections from input String.
fn generate_graph(input: &String) -> (usize, usize, (isize, isize), HashMap<(isize, isize), Vec<(isize, isize)>>) {

    let rows = (*input).trim().lines().count();
    let cols = (*input).trim().lines().next().expect("Must have at least one row.").chars().count();

    let mut connections = vec![];
    let mut s_loc = (0_isize, 0_isize);
    for (r, line) in input.lines().enumerate() {
        let r = r as isize;
        for (c, pipe) in line.chars().enumerate() {
            let c = c as isize;
            connections.push({
                let connections = match pipe {
                    '|' => vec![(r - 1, c), (r + 1, c)],
                    '-' => vec![(r, c - 1), (r, c + 1)],
                    'L' => vec![(r - 1, c), (r, c + 1)],
                    'J' => vec![(r - 1, c), (r, c - 1)],
                    '7' => vec![(r, c - 1), (r + 1, c)],
                    'F' => vec![(r + 1, c), (r, c + 1)],
                    'S' => {
                        s_loc = (r, c);
                        vec![]
                    },
                    _ => vec![],
                    }
                    .into_iter()
                    .filter(|cell| check_bounds(rows, cols, *cell))
                    .collect::<Vec<_>>();
                    
                ((r, c), connections)
            })
        }
    }
    (rows, cols, s_loc, connections.into_iter().collect::<HashMap<(isize, isize), Vec<(isize, isize)>>>())
}

fn solution_p1(input: String) -> usize {

    let (rows, cols, s_loc, graph) = generate_graph(&input);

    let mut s_connections = vec![
        (s_loc.0 - 1, s_loc.1),
        (s_loc.0 + 1, s_loc.1), 
        (s_loc.0, s_loc.1 - 1), 
        (s_loc.0, s_loc.1 + 1)]
        .into_iter()
        .filter(|check|
                check_bounds(rows, cols, *check) && 
                graph.get(check).expect("Must have valid pipe data.")
                    .iter()
                    .any(|neighbour| *neighbour == s_loc));

    let mut start_side = s_connections.next().expect("Must have one connection.");
    let mut prev = s_loc;
    let mut cycle_length = 0_usize;
    while start_side != s_loc {
        let next = graph
            .get(&start_side).expect("Must be a valid pipe.")
            .iter()
            .filter(|&neighbour| *neighbour != prev)
            .next().expect("Must have other connection.");

        cycle_length += 1;

        prev = start_side;
        start_side = *next;
    }

    (cycle_length + 1) / 2

}

fn solution_p2(input: String) -> usize {

    let (rows, cols, s_loc, graph) = generate_graph(&input);

    let mut s_connections = vec![
        (s_loc.0 - 1, s_loc.1),
        (s_loc.0 + 1, s_loc.1), 
        (s_loc.0, s_loc.1 - 1), 
        (s_loc.0, s_loc.1 + 1)]
        .into_iter()
        .filter(|check|
                check_bounds(rows, cols, *check) && 
                graph.get(check).expect("Must have valid pipe data.")
                    .iter()
                    .any(|neighbour| *neighbour == s_loc));

    let start_side = s_connections.next().expect("Must have one connection.");
    let mut cell = start_side.clone();
    let mut prev = s_loc;

    // first pass to figure out where pipes are
    let mut pipes = vec![s_loc].into_iter().collect::<HashSet<_>>();
    while cell != s_loc {
        let next = graph
            .get(&cell).expect("Must be a valid pipe.")
            .iter()
            .filter(|&neighbour| *neighbour != prev)
            .next().expect("Must have other connection.");

        pipes.insert(cell);

        prev = cell;
        cell = *next;
    }

    // check for casting rays left and right of pipes
    // if a ray hits the edge of the map space, we need to use the other direction
    'check_dirs: for (dr_mul, dc_mul) in [(1, -1), (-1, 1)] {
        let mut interior: HashSet<(isize, isize)> = HashSet::new();
        cell = start_side.clone();
        prev = s_loc;
        let mut prev_dir = (0_isize, 0_isize);

        while cell != s_loc {
            let next = graph
                .get(&cell).expect("Must be a valid pipe.")
                .iter()
                .filter(|&neighbour| *neighbour != prev)
                .next().expect("Must have other connection.");
    
            // "cast a ray" from the pipe until you hit another pipe
            // add any cells in between to interior
            let dr = dr_mul * (cell.1 - prev.1);
            let dc = dc_mul * (cell.0 - prev.0);
    
            let mut check_cell = (cell.0 + dr, cell.1 + dc);
            while !pipes.contains(&check_cell) {
                if !check_bounds(rows, cols, check_cell) {
                    continue 'check_dirs;  // must be capturing the outside cells instead of inside, switch to other direction
                }

                interior.insert(check_cell);
                check_cell = (check_cell.0 + dr, check_cell.1 + dc);
            }

            if prev_dir != (dr, dc) {
                // cast ray on previous cell too
                // catch edge cases
                check_cell = (prev.0 + dr, prev.1 + dc);
                while !pipes.contains(&check_cell) {
                    if !check_bounds(rows, cols, check_cell) {
                        continue 'check_dirs;  // must be capturing the outside cells instead of inside, switch to other direction
                    }
    
                    interior.insert(check_cell);
                    check_cell = (check_cell.0 + dr, check_cell.1 + dc);
                }
            }
    
            prev = cell;
            cell = *next;
            prev_dir = (dr, dc);
        }
    
        return interior.len();
    }

    0

}


#[cfg(test)]
mod tests {
    use crate::day10::{solution_p1, solution_p2};

    const EXAMPLE_1_BARE: &str = ".....\n.S-7.\n.|.|.\n.L-J.\n.....\n";
    const EXAMPLE_1_FILLED: &str = "-L|F7\n7S-7|\nL|7||\n-L-J|\nL|-JF\n";
    const EXAMPLE_2_BARE: &str = "..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...\n";
    const EXAMPLE_2_FILLED: &str = "7-F7-\n.FJ|7\nSJLL7\n|F--J\nLJ.LJ\n";

    const EXAMPLE_3: &str = "...........\n.S-------7.\n.|F-----7|.\n.||.....||.\n.||.....||.\n.|L-7.F-J|.\n.|..|.|..|.\n.L--J.L--J.\n...........\n";
    const EXAMPLE_4: &str = ".F----7F7F7F7F-7....\n.|F--7||||||||FJ....\n.||.FJ||||||||L7....\nFJL7L7LJLJ||LJ.L-7..\nL--J.L7...LJS7F-7L7.\n....F-J..F7FJ|L7L7L7\n....L7.F7||L7|.L7L7|\n.....|FJLJ|FJ|F7|.LJ\n....FJL-7.||.||||...\n....L---J.LJ.LJLJ...\n";
    const EXAMPLE_5: &str = "FF7FSF7F7F7F7F7F---7\nL|LJ||||||||||||F--J\nFL-7LJLJ||||||LJL-77\nF--JF--7||LJLJ7F7FJ-\nL---JF-JLJ.||-FJLJJ7\n|F|F-JF---7F7-L7L|7|\n|FFJF7L7F-JF7|JL---7\n7-L-JL7||F7|L7F-7F7|\nL.L7LFJ|||||FJL7||LJ\nL7JLJL-JLJLJL--JLJ.L\n";

    #[test]
    fn pt1_1_bare() {
        let input = String::from(EXAMPLE_1_BARE);
        assert_eq!(solution_p1(input), 4);
    }

    #[test]
    fn pt1_1_filled() {
        let input = String::from(EXAMPLE_1_FILLED);
        assert_eq!(solution_p1(input), 4);
    }

    #[test]
    fn pt1_2_bare() {
        let input = String::from(EXAMPLE_2_BARE);
        assert_eq!(solution_p1(input), 8);
    }

    #[test]
    fn pt1_2_filled() {
        let input = String::from(EXAMPLE_2_FILLED);
        assert_eq!(solution_p1(input), 8);
    }

    #[test]
    fn pt2_1() {
        let input = String::from(EXAMPLE_3);
        assert_eq!(solution_p2(input), 4);
    }

    #[test]
    fn pt2_2() {
        let input = String::from(EXAMPLE_4);
        assert_eq!(solution_p2(input), 8);
    }

    #[test]
    fn pt2_3() {
        let input = String::from(EXAMPLE_5);
        assert_eq!(solution_p2(input), 10);
    }
}
