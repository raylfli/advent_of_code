use std::collections::{HashMap, HashSet};

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Upsert to hash map
fn upsert(hm: &mut HashMap<(isize, isize), HashSet<(isize, isize)>>, k: (isize, isize), v: (isize, isize)) {

    if hm.contains_key(&k) {
        hm.get_mut(&k).unwrap().insert(v);
    } else {
        hm.insert(k, HashSet::from([v]));
    }

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

    let n_rows = map.len() as isize;
    let n_cols = map[0].len() as isize;

    let start = (0_isize, map[0].iter().position(|c| *c == '.').expect("Must have a start coordinate.") as isize);
    let end = ((n_rows - 1) as isize, map[(n_rows - 1) as usize].iter().position(|c| *c == '.').expect("Must have an end coordinate.") as isize);

    // topological sort for https://en.wikipedia.org/wiki/Longest_path_problem#Acyclic_graphs

    let mut children: HashMap<(isize, isize), HashSet<(isize, isize)>> = HashMap::new();
    let mut frontier: Vec<(isize, isize, isize, isize)> = vec![(start.0, start.1, -1, -1)]; // (r, c, prev_r, prev_c)
    while frontier.len() > 0 {
        let (r, c, pr, pc) = frontier.pop().unwrap();

        match map[r as usize][c as usize] {
            '^' => {
                frontier.push((r - 1, c, r, c));
                upsert(&mut children, (pr, pc), (r, c));
            },
            'v'=> {
                frontier.push((r + 1, c, r, c));
                upsert(&mut children, (pr, pc), (r, c));
            },
            '>' => {
                frontier.push((r, c + 1, r, c));
                upsert(&mut children, (pr, pc), (r, c));
            },
            '<' => {
                frontier.push((r, c - 1, r, c));
                upsert(&mut children, (pr, pc), (r, c));
            },
            '.' => {
                for (dr, dc, arrow) in [
                    (0_isize, 1_isize, '>'),
                    (0_isize, -1_isize, '<'),
                    (1_isize, 0_isize, 'v'),
                    (-1_isize, 0_isize, '^'),
                ] {
                    let (cr, cc) = (r + dr, c + dc);
                    if (cr, cc) != (pr, pc) &&
                        cr >= 0 &&
                        cr < n_rows &&
                        cc >= 0 &&
                        cc < n_cols &&
                        (map[cr as usize][cc as usize] == '.' || map[cr as usize][cc as usize] == arrow){
                        frontier.push((cr, cc, r, c));
                    }
                }
                upsert(&mut children, (pr, pc), (r, c));
            },
            _ => {},
        }
    }

    // topological sort
    let mut topo_order: Vec<(isize, isize)> = vec![];
    let mut no_incoming: HashSet<(isize, isize)> = HashSet::from([start]);
    let mut graph = children.clone();
    graph.remove(&(-1, -1));
    while no_incoming.len() > 0 {
        let n = *no_incoming.iter().next().unwrap();
        no_incoming.remove(&n);
        topo_order.push(n.clone());
        
        let empty_hs: HashSet::<(isize, isize)> = HashSet::new();
        let neighbours = graph.remove(&n).unwrap_or(empty_hs);
        for neighbour in neighbours {
            if graph.values().filter(|&v| v.contains(&neighbour)).collect_vec().len() == 0 {
                no_incoming.insert(neighbour);
            }
        }
    }

    // find longest path
    let topo_map = topo_order.iter().enumerate().map(|n| (*n.1, n.0)).collect::<HashMap<(isize, isize), usize>>();
    let mut length: Vec<usize> = vec![0; topo_order.len()];
    length[0] = 0;
    for (i, node) in topo_order.iter().enumerate() {
        if let Some(neighbours) = children.get(node) {
            for neighbour in neighbours {
                if let Some(length_i) = topo_map.get(neighbour) {
                    length[*length_i] = length[*length_i].max(length[i] + 1);
                }
            }
        }
    }

    length[*topo_map.get(&end).unwrap()]

}

/// DFS visit
fn visit(
    longest: &mut HashMap<(isize, isize), usize>,
    visited: &mut HashMap<(isize, isize), bool>,
    edges: &HashMap<(isize, isize), HashSet<((isize, isize), usize)>>,
    node: (isize, isize),
    len: usize,
) {
    if let Some(v) = visited.get(&node) {
        if *v {
            return;
        }
    }

    visited.insert(node, true);

    let prev_longest = longest.get_mut(&node);
    if let Some(prev_longest) = prev_longest {
        *prev_longest = (*prev_longest).max(len);
    } else {
        longest.insert(node, len);
    }

    if node == (140, 139) {
        visited.insert(node, false);
        return;
    }

    let neighbours = edges.get(&node);
    if let Some(neighbours) = neighbours {
        for (n, n_len) in neighbours {
            visit(longest, visited, edges, *n, len + *n_len);
        }
    }

    visited.insert(node, false);
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

    let n_rows = map.len() as isize;
    let n_cols = map[0].len() as isize;

    let start = (0_isize, map[0].iter().position(|c| *c == '.').expect("Must have a start coordinate.") as isize);
    let end = ((n_rows - 1) as isize, map[(n_rows - 1) as usize].iter().position(|c| *c == '.').expect("Must have an end coordinate.") as isize);

    // find junction points for edge contraction
    let mut junctions: HashSet<(isize, isize)> = HashSet::new();
    junctions.insert(start);
    junctions.insert(end);
    for (r, row) in map.iter().enumerate() {
        for (c, col) in row.iter().enumerate() {
            let r = r as isize;
            let c = c as isize;
            let mut count = 0_usize;
            for (dr, dc) in [
                (0_isize, 1_isize),
                (0_isize, -1_isize),
                (1_isize, 0_isize, ),
                (-1_isize, 0_isize),
            ] {
                let (cr, cc) = (r + dr, c + dc);
                if *col != '#' && cr >= 0 && cr < n_rows && cc >= 0 && cc < n_cols && map[cr as usize][cc as usize] != '#' {
                    count += 1;
                }
            }
            if count > 2 {
                junctions.insert((r, c));
            }
        }
    }

    let mut lengths: HashMap<(isize, isize), HashSet<((isize, isize), usize)>> = HashMap::new();
    // find lengths between junctions
    for (jr, jc) in junctions.iter() {
        let jr = *jr;
        let jc = *jc;
        let mut frontier: Vec<(isize, isize, isize, isize, usize)> = vec![
            (jr, jc, 0, 1, 0),
            (jr, jc, 0, -1, 0),
            (jr, jc, 1, 0, 0),
            (jr, jc, -1, 0, 0),
        ];

        while frontier.len() > 0 {
            let (r, c, dr, dc, steps) = frontier.pop().unwrap();

            if r >= 0 && r < n_rows && c >= 0 && c < n_cols {
                if map[r as usize][c as usize] != '#' {
                    if steps > 0 && junctions.contains(&(r, c)) {
                        if lengths.contains_key(&(jr, jc)) {
                            lengths.get_mut(&(jr, jc)).unwrap().insert(((r, c), steps));
                        } else {
                            lengths.insert((jr, jc), HashSet::from([((r, c), steps)]));
                        }
                    } else {
                        for (dr2, dc2) in [
                            (0_isize, 1_isize),
                            (0_isize, -1_isize),
                            (1_isize, 0_isize, ),
                            (-1_isize, 0_isize),
                        ] {
                            if (dr, dc) != (-dr2, -dc2) {
                                frontier.push((r + dr2, c + dc2, dr2, dc2, steps + 1));
                            }
                        }
                    }
                }
            }
        }
    }

    // brute force for longest path
    let mut longest: HashMap<(isize, isize), usize> = HashMap::new();
    let mut visited: HashMap<(isize, isize), bool> = HashMap::new();
    visit(&mut longest, &mut visited, &lengths, start, 0);

    *longest.get(&end).expect("Must have longest path to exit.")

}


#[cfg(test)]
mod tests {
    use crate::day23::{solution_p1, solution_p2};

    const EXAMPLE: &str = "#.#####################\n#.......#########...###\n#######.#########.#.###\n###.....#.>.>.###.#.###\n###v#####.#v#.###.#.###\n###.>...#.#.#.....#...#\n###v###.#.#.#########.#\n###...#.#.#.......#...#\n#####.#.#.#######.#.###\n#.....#.#.#.......#...#\n#.#####.#.#.#########v#\n#.#...#...#...###...>.#\n#.#.#v#######v###.###v#\n#...#.>.#...>.>.#.###.#\n#####v#.#.###v#.#.###.#\n#.....#...#...#.#.#...#\n#.#########.###.#.#.###\n#...###...#...#...#.###\n###.###.#.###v#####v###\n#...#...#.#.>.>.#.>.###\n#.###.###.#.###.#.#v###\n#.....###...###...#...#\n#####################.#\n";

    const SMALL_EXAMPLE: &str = "#.#######\n#.......#\n#######.#\n###.....#\n###v#####\n###.>...#\n###v###.#\n###...#.#\n#####.#.#\n";

    #[test]
    fn small() {
        let input = String::from(SMALL_EXAMPLE);
        assert_eq!(solution_p1(input), 20);
    }

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 94);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 154);
    }

}
