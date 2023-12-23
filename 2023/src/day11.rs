use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Calculate the pair wise distances between galaxies given the input image and dilation factor.
fn galaxy_dist(input: String, dilation: usize) -> usize {

    let rows = input.trim().lines().count();
    let cols = input.trim().lines().next().expect("Must have at least one row.").chars().count();

    // find galaxies and empty rows
    let mut empty_rows: Vec<bool> = vec![true; rows];
    let mut empty_cols: Vec<bool> = vec![true; cols];
    let mut galaxies: Vec<(usize, usize)> = vec![];
    for (r, line) in input.lines().enumerate() {
        for (c, pixel) in line.chars().enumerate() {
            if pixel == '#' {
                galaxies.push((r, c));
                empty_rows[r] = false;
                empty_cols[c] = false;
            }
        } 
    }

    // remap galaxy coordinates based on empty rows and columns
    {
        // remap columns
        galaxies.sort_by(|g1, g2| g1.1.cmp(&g2.1));
        let mut new_galaxies: Vec<(usize, usize)> = vec![(0, 0); galaxies.len()];
        let mut d = 0;
        let mut i = 0;
        for (col, empty) in empty_cols.into_iter().enumerate() {
            if empty {
                d += dilation - 1;
            }
            while i < galaxies.len() && galaxies[i].1 == col {
                new_galaxies[i] = (galaxies[i].0, galaxies[i].1 + d);
                i += 1;
            }
        }
        galaxies = new_galaxies;
    }
    {
        // remap rows
        galaxies.sort_by(|g1, g2| g1.0.cmp(&g2.0));
        let mut new_galaxies: Vec<(usize, usize)> = vec![(0, 0); galaxies.len()];
        let mut d = 0;
        let mut i = 0;
        for (row, empty) in empty_rows.into_iter().enumerate() {
            if empty {
                d += dilation - 1;
            }
            while i < galaxies.len() && galaxies[i].0 == row {
                new_galaxies[i] = (galaxies[i].0 + d, galaxies[i].1);
                i += 1;
            }
        }
        galaxies = new_galaxies;
    }

    galaxies
        .into_iter()
        .tuple_combinations()
        .map(|((r1, c1), (r2, c2))| {
            let r1 = r1 as i64;
            let c1 = c1 as i64;
            let r2 = r2 as i64;
            let c2 = c2 as i64;
            ((r2 - r1).abs() + (c2 - c1).abs()) as usize
        })
        .sum()

}

fn solution_p1(input: String) -> usize {

    galaxy_dist(input, 2)

}


fn solution_p2(input: String) -> usize {

    galaxy_dist(input, 1_000_000)

}


#[cfg(test)]
mod tests {
    use crate::day11::{solution_p1, galaxy_dist};

    const EXAMPLE: &str = "...#......\n.......#..\n#.........\n..........\n......#...\n.#........\n.........#\n..........\n.......#..\n#...#.....\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 374);
    }

    #[test]
    fn pt2_d10() {
        let input = String::from(EXAMPLE);
        assert_eq!(galaxy_dist(input, 10), 1030);
    }

    #[test]
    fn pt2_d100() {
        let input = String::from(EXAMPLE);
        assert_eq!(galaxy_dist(input, 100), 8410);
    }

}
