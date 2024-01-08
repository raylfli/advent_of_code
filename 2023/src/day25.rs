use std::collections::{HashMap, HashSet};

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Upsert into graph
fn upsert(hm: &mut HashMap<usize, HashMap<usize, usize>>, k: usize, v: usize, w: usize) {

    if hm.contains_key(&k) {
        hm.get_mut(&k).unwrap().insert(v, w);
    } else {
        hm.insert(k, HashMap::from([(v, w)]));
    }

}

/// Remove edge from graph
/// 
/// Returns the weight of the edge if it existed.
fn remove(hm: &mut HashMap<usize, HashMap<usize, usize>>, a: usize, b: usize) -> Option<usize> {

    if hm.contains_key(&a) && hm.contains_key(&b) {
        let ab = hm.get_mut(&a).unwrap().remove(&b);
        let ba = hm.get_mut(&b).unwrap().remove(&a);
        match (ab, ba) {
            (Some(ab), Some(_ba)) => { return Some(ab); },
            _ => { return None; },
        }
    } else {
        return None;
    }

}

/// Find min st cut of graph with at least one edge.
/// 
/// Returns (s, t, min cut)
fn min_st_cut(
    edges: &HashMap<usize, HashMap<usize, usize>>,
    first: usize,
) -> (usize, usize, usize) {

    let mut subset: HashSet<usize> = HashSet::from([first]);
    let mut subset_vec: Vec<usize> = vec![first];
    let mut weights: Vec<usize> = vec![];
    let mut candidates = edges.iter().filter(|(_k, v)| v.len() > 0).map(|kv| *kv.0).collect::<HashSet<_>>();
    candidates.remove(&first);
    while candidates.len() > 0 {
        let mut i = 0;
        let mut max_weight = isize::MIN;
        for cand in candidates.iter() {
            let weight: usize = edges
                .get(cand).expect("Candidate must have outgoing edge.")
                .iter()
                .filter(|(dest, _w)| subset.contains(*dest))
                .map(|(_dest, w)| *w)
                .sum();

            if weight as isize > max_weight {
                max_weight = weight as isize;
                i = *cand;
            }
        }

        candidates.remove(&i);
        subset.insert(i);
        subset_vec.push(i);
        weights.push(max_weight as usize);
    }

    (
        subset_vec[subset_vec.len() - 2],
        subset_vec[subset_vec.len() - 1],
        weights[weights.len() - 1],
    )

}

/// Stoer-Wagner algorithm for a 3-edge connected graph
/// 
/// Returns the size of the two partitions around the min cut of 3
fn stoer_wagner(mut edges: HashMap<usize, HashMap<usize, usize>>) -> (usize, usize) {

    let n = edges.len();

    let mut rep: HashMap<usize, usize> = edges
        .keys()
        .map(|k| (*k, 1))
        .collect::<HashMap<usize, usize>>();

    let mut curr_part: HashSet<usize> = HashSet::new();
    // let mut curr_best_part: Option<HashSet<usize>> = None;
    let mut curr_best_cut: Option<(usize, usize, usize)> = None;
    while edges.values().map(|hm| hm.len()).sum::<usize>() > 2 {
        let (s, t, cut) = min_st_cut(&edges, 0);
        if curr_best_cut == None || cut < curr_best_cut.unwrap().2 {
            curr_best_cut = Some((s, t, cut));
            // curr_best_part = Some(curr_part.clone());
            // curr_best_part.as_mut().unwrap().insert(t);
        }
        curr_part.insert(t);

        *rep.get_mut(&s).unwrap() += *rep.get(&t).unwrap();
    
        let s_neighbours = edges.get(&s).expect("Vertex must have edges.").keys().map(|n| *n).collect::<HashSet<_>>();
        let t_neighbours = edges.get(&t).expect("Vertex must have edges.").keys().map(|n| *n).collect::<HashSet<_>>();

        if cut == 3 {
            return (n - *rep.get(&t).unwrap(), *rep.get(&t).unwrap());
        }

        for neighbour in t_neighbours {
            if neighbour == s {
                remove(&mut edges, s, t);
            } else if s_neighbours.contains(&neighbour) {
                let wt = remove(&mut edges, t, neighbour).unwrap();
                let ws = remove(&mut edges, s, neighbour).unwrap();
                upsert(&mut edges, s, neighbour, wt + ws);
                upsert(&mut edges, neighbour, s, wt + ws);
            } else {
                let w = remove(&mut edges, t, neighbour).unwrap();
                upsert(&mut edges, s, neighbour, w);
                upsert(&mut edges, neighbour, s, w);
            }
        }
    }

    (0, 0)

}

fn solution_p1(input: String) -> usize {

    // mincut/maxcut problem
    // https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm
    // https://blog.thomasjungblut.com/graph/mincut/mincut/

    let mut vertices: Vec<&str> = vec![];
    let mut id_to_i: HashMap<&str, usize> = HashMap::new();
    let mut edges_vec: Vec<(usize, HashSet<usize>)> = vec![];
    for line in input.lines() {
        let mut components = line.split(':');
        let from = components.next().expect("Must have from component.");
        if !id_to_i.contains_key(from) {
            id_to_i.insert(from, vertices.len());
            vertices.push(from);
        }
        let to = components.next().expect("Must have to components.").trim().split(' ');
        let mut hs: HashSet<usize> = HashSet::new();
        for comp in to {
            if !id_to_i.contains_key(comp) {
                id_to_i.insert(comp, vertices.len());
                vertices.push(comp);
            }
            hs.insert(*id_to_i.get(comp).unwrap());
        }
        edges_vec.push((*id_to_i.get(from).unwrap(), hs));
    }

    let mut edges: HashMap<usize, HashMap<usize, usize>> = HashMap::new();
    for (from, tos) in edges_vec.into_iter() {
        for to in tos {
            upsert(&mut edges, to, from, 1);
            upsert(&mut edges, from, to, 1);
        }
    }

    // Stoer-Wagner algorithm
    let (left, right) = stoer_wagner(edges);
    
    left * right

}

fn solution_p2(_input: String) -> usize {

    // no part 2 puzzle!
    0

}


#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use crate::day25::{solution_p1, solution_p2, min_st_cut};

    const EXAMPLE: &str = "jqt: rhn xhk nvd\nrsh: frs pzl lsr\nxhk: hfx\ncmg: qnr nvd lhk bvb\nrhn: xhk bvb hfx\nbvb: xhk hfx\npzl: lsr hfx nvd\nqnr: nvd\nntq: jqt hfx bvb xhk\nnvd: lhk\nlsr: lhk\nrzs: qnr cmg lsr rsh\nfrs: qnr lhk lsr\n";

    #[test]
    fn test_min_st_cut() {
        let hm: HashMap<usize, HashMap<usize, usize>> = HashMap::from([
            (0, HashMap::from([(1, 4), (2, 5)])),
            (1, HashMap::from([(0, 4), (2, 3)])),
            (2, HashMap::from([(0, 5), (1, 3)])),
        ]);
        assert_eq!(min_st_cut(&hm, 0), (2, 1, 7));
    }

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 54);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 0);
    }

}
