use std::collections::HashMap;

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Calculate the north load on the dish.
fn calculate_north_load(dish: &Vec<Vec<char>>) -> usize {

    let n_rows = dish.len();

    let mut weight = 0_usize;
    for (r, row) in dish.iter().enumerate() {
        for mirror in row.iter() {
            match *mirror {
                'O' => weight += n_rows - r,
                _ => {}
            }
        }
    }

    weight

}

/// Generate representative string.
fn generate_rep_string(dish: &Vec<Vec<char>>) -> String {

    dish
        .iter()
        .map(|row| row.iter().join(""))
        .join("\n")

}

fn solution_p1(input: String) -> usize {

    let dish = input
        .lines()
        .map(|line| {
            line
                .chars()
                .collect_vec()
            }
        )
        .collect_vec();

    let n_rows = dish.len();
    let n_cols = dish[0].len();

    let mut new_dish = vec![vec!['.'; n_cols]; n_rows];

    // north
    for c in 0..n_cols {
        let mut i = 0_usize;  // next rock space
        for (r, row) in dish.iter().enumerate() {
            let mirror = row[c];
            match mirror {
                '#' => {
                    new_dish[r][c] = '#';
                    i = r + 1;
                },
                'O' => {
                    new_dish[i][c] = 'O';
                    i += 1;
                },
                _ => {}
            }
        }
    }

    calculate_north_load(&new_dish)

}

fn solution_p2(input: String) -> usize {

    let mut dish = input
        .lines()
        .map(|line| {
            line
                .chars()
                .collect_vec()
            }
        )
        .collect_vec();

    let n_rows = dish.len();
    let n_cols = dish[0].len();
    
    let mut new_dish = vec![vec!['.'; n_cols]; n_rows];
    
    let mut state_load: HashMap<String, usize> = HashMap::new(); // state string -> index
    let mut states = vec![]; // all states

    let prev_str = generate_rep_string(&dish);
    states.push(prev_str.clone());
    state_load.insert(prev_str, 0);

    const NUM_CYCLES: usize = 1_000_000_000;

    for cycle in 0..NUM_CYCLES {

        // north
        for c in 0..n_cols {
            let mut i = 0_usize;  // next rock space
            for (r, row) in dish.iter().enumerate() {
                let mirror = row[c];
                match mirror {
                    '#' => {
                        new_dish[r][c] = '#';
                        i = r + 1;
                    },
                    'O' => {
                        new_dish[i][c] = 'O';
                        i += 1;
                    },
                    _ => {}
                }
            }
        }
        dish = new_dish;
        new_dish = vec![vec!['.'; n_cols]; n_rows];

        // west
        for (r, row) in dish.iter().enumerate() {
            let mut i = 0_usize;  // next rock space
            for (c, mirror) in row.iter().enumerate() {
                match *mirror {
                    '#' => {
                        new_dish[r][c] = '#';
                        i = c + 1;
                    },
                    'O' => {
                        new_dish[r][i] = 'O';
                        i += 1;
                    },
                    _ => {}
                }
            }
        }
        dish = new_dish;
        new_dish = vec![vec!['.'; n_cols]; n_rows];
        
        // south
        for c in 0..n_cols {
            let mut i = (n_rows - 1) as isize;  // next rock space
            for (r, row) in dish.iter().enumerate().rev() {
                let mirror = row[c];
                match mirror {
                    '#' => {
                        new_dish[r][c] = '#';
                        i = (r as isize) - 1;
                    },
                    'O' => {
                        new_dish[i as usize][c] = 'O';
                        i -= 1;
                    },
                    _ => {}
                }
            }
        }
        dish = new_dish;
        new_dish = vec![vec!['.'; n_cols]; n_rows];

        // east
        for (r, row) in dish.iter().enumerate() {
            let mut i = (n_cols - 1) as isize;  // next rock space
            for (c, mirror) in row.iter().enumerate().rev() {
                match *mirror {
                    '#' => {
                        new_dish[r][c] = '#';
                        i = (c as isize) - 1;
                    },
                    'O' => {
                        new_dish[r][i as usize] = 'O';
                        i -= 1;
                    },
                    _ => {}
                }
            }
        }

        let s = generate_rep_string(&new_dish);

        // check for cycle
        if state_load.contains_key(&s) {
            let seen_cycle = state_load.get(&s).expect("Must have seen cycle before.");
            let cycle_length = cycle + 1- seen_cycle;
            let remaining_cycles = (NUM_CYCLES - seen_cycle) % cycle_length;
            let final_state = states[seen_cycle + remaining_cycles]
                .lines()
                .map(|line| {
                    line
                        .chars()
                        .collect_vec()
                    }
                )
                .collect_vec();
            return calculate_north_load(&final_state);
        }

        states.push(s.clone());
        state_load.insert(s, cycle + 1);

        dish = new_dish;
        new_dish = vec![vec!['.'; n_cols]; n_rows];
    }

    0

}


#[cfg(test)]
mod tests {
    use itertools::Itertools;

    use crate::day14::{solution_p1, solution_p2, calculate_north_load};

    const EXAMPLE: &str = "O....#....\nO.OO#....#\n.....##...\nOO.#O....O\n.O.....O#.\nO.#..O.#.#\n..O..#O..O\n.......O..\n#....###..\n#OO..#....\n";

    #[test]
    fn north_load_1() {
        let dish_str = String::from(".....#....\n....#...O#\n.....##...\n...#......\n.....OOO#.\n.O#...O#.#\n....O#...O\n......OOOO\n#....###.O\n#.OOO#..OO");
        let dish = dish_str
            .lines()
            .map(|line| {
                line
                    .chars()
                    .collect_vec()
                }
            )
            .collect_vec();
        assert_eq!(calculate_north_load(&dish), 64);
    }

    #[test]
    fn north_load_2() {
        let dish_str = String::from("OOOO.#.O..\nOO..#....#\nOO..O##..O\nO..#.OO...\n........#.\n..#....#.#\n..O..#.O.O\n..O.......\n#....###..\n#....#....");
        let dish = dish_str
            .lines()
            .map(|line| {
                line
                    .chars()
                    .collect_vec()
                }
            )
            .collect_vec();
        assert_eq!(calculate_north_load(&dish), 136);
    }

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 136);
    }
    

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 64);
    }

}
