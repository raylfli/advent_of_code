use std::collections::{HashMap, HashSet, VecDeque};

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Parse input and generate:
/// 
/// 1. Vector of blocks and their bounds
/// 2. Parent pointer graph of block parents (blocks that are underneath)
/// 3. Dependency graph of block children (blocks that are above)
fn get_parents_children(input: String) -> (Vec<((u32, u32, u32), (u32, u32, u32))>, HashMap<usize, HashSet<usize>>, HashMap<usize, HashSet<usize>>) {
    
    type Coordinate = u32;
    type Point = (Coordinate, Coordinate, Coordinate);

    let mut blocks = input
        .lines()
        .map(|line| {
            let mut points = line.split('~');
            let p1: Point = points
                .next().expect("Must have first point.")
                .split(',')
                .map(|n| {
                    n.parse::<Coordinate>().expect("Must have valid coordinate.")
                })
                .collect_tuple().expect("Point must be of dimension 3.");
            let p2: Point = points
                .next().expect("Must have second point.")
                .split(',')
                .map(|n| {
                    n.parse::<Coordinate>().expect("Must have valid coordinate.")
                })
                .collect_tuple().expect("Point must be of dimension 3.");
            (p1, p2)
        })
        .collect_vec();

    blocks.sort_unstable_by_key(|(p1, _p2)| p1.2);

    let mut height_grid = [[-1_isize; 10]; 10];

    // parent pointer graph
    let mut parents: HashMap<usize, HashSet<usize>> = HashMap::new();
    for i in 0..blocks.len() {
        let p1 = blocks[i].0;
        let p2 = blocks[i].1;
    
        // find highest cell underneath
        let mut max_z = 0_u32;
        for x in p1.0..=p2.0 {
            for y in p1.1..=p2.1 {
                let grid_i = height_grid[x as usize][y as usize];
                if grid_i >= 0 && blocks[grid_i as usize].1.2 > max_z {
                    max_z = blocks[grid_i as usize].1.2;
                }
            }
        }

        let mut underneath: HashSet<usize> = HashSet::new();
        for x in p1.0..=p2.0 {
            for y in p1.1..=p2.1 {
                let grid_i = height_grid[x as usize][y as usize];
                if grid_i >= 0 && blocks[grid_i as usize].1.2 == max_z {
                    underneath.insert(grid_i as usize);
                }
                height_grid[x as usize][y as usize] = i as isize;
            }
        }
        let d = blocks[i].1.2 - blocks[i].0.2;
        blocks[i].0.2 = max_z + 1;
        blocks[i].1.2 = max_z + 1 + d;
        parents.insert(i, underneath);
    }

    let mut children: HashMap<usize, HashSet<usize>> = HashMap::new();
    for (block, dependees) in parents.iter() {
        for dep in dependees.iter() {
            if children.contains_key(dep) {
                children.get_mut(dep).unwrap().insert(*block);
            } else {
                children.insert(*dep, HashSet::from([*block]));
            }
        }
    }
    (blocks, parents, children)
}

fn solution_p1(input: String) -> usize {

    let (blocks, parents, children) = get_parents_children(input);

    let mut count = 0_usize;
    for block in 0..blocks.len() {
        let dependents = children.get(&block);
        if let Some(dependents) = dependents {
            if dependents.iter().all(|dep| parents[dep].len() > 1) {
                count += 1;
            }
        } else {
            count += 1;
        }
    }

    count

}

fn solution_p2(input: String) -> usize {

    let (blocks, parents, children) = get_parents_children(input);

    let mut total = 0_usize;

    for block in 0..blocks.len() {
        // BFS to go layer by layer propagating disintegrations
        let mut visited: HashSet<usize> = HashSet::from([block]);
        let mut frontier: VecDeque<usize> = VecDeque::from([block]);
        let on_top = children.get(&block);
        if let Some(on_top) = on_top {
            for child in on_top {
                frontier.push_back(*child);
            }
        }
        while frontier.len() > 0 {
            let i = frontier.pop_front().unwrap();
            if !visited.contains(&i) {
                if parents.get(&i).expect("Block must have parents.").iter().all(|par| visited.contains(par)) {
                    visited.insert(i);
                    let on_top = children.get(&i);
                    if let Some(on_top) = on_top {
                        for child in on_top {
                            frontier.push_back(*child);
                        }
                    }
                }
            }
        }
        total += visited.len() - 1;
    }

    total

}


#[cfg(test)]
mod tests {
    use crate::day22::{solution_p1, solution_p2};

    const EXAMPLE: &str = "1,0,1~1,2,1\n0,0,2~2,0,2\n0,2,3~2,2,3\n0,0,4~0,2,4\n2,0,5~2,2,5\n0,1,6~2,1,6\n1,1,8~1,1,9\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 5);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 7);
    }

}
