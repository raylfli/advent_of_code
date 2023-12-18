use std::cmp;

const REDS: u8 = 12;
const GREENS: u8 = 13;
const BLUES: u8 = 14;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

/// Returns the game information for one cube draw in the format (r, g, b).
fn parse_game(game: &str) -> (u8, u8, u8) {
    let mut n_red: u8 = 0;
    let mut n_green: u8 = 0;
    let mut n_blue: u8 = 0;

    for draw in game.split(",") {
        let mut cube = draw.trim().split(" ");
        let n = cube.next().expect("Cube pull info should have at least 2 parts.")
            .trim().parse::<u8>().expect("Cube pull number should be a number.");
        let colour = cube.next().expect("Cube pull info should have at least 2 parts.");

        match colour.trim() {
            "red" => n_red += n,
            "green" => n_green += n,
            "blue" => n_blue += n,
            _ => (),
        }
    }

    (n_red, n_green, n_blue)
}

/// Returns whether the game is valid.
fn valid_game(draws: impl Iterator<Item = (u8, u8, u8)>) -> bool {

    for game in draws {
        if game.0 > REDS || game.1 > GREENS || game.2 > BLUES {
            return false;
        }
    }
    true
}

fn solution_p1(input: String) -> u32 {
    let mut total: u32 = 0;
    for line in input.lines() {

        let game_id = line.split(":").next().expect("Game line should include a colon.")
            .split(" ").last().expect("Game ID part should include two parts.")
            .parse::<u8>().expect("Game ID should be an integer.");

        let draws = line.split(":").last().expect("Game line should include a colon.")
            .split(";").map(parse_game);

        if valid_game(draws) {
            total += game_id as u32;
        }
    }

    total

}

/// Compute the minimum number of cubes needed for this game.
fn min_cubes(draws: impl Iterator<Item = (u8, u8, u8)>) -> [u8; 3] {

    let mut n_red = u8::MIN;
    let mut n_green = u8::MIN;
    let mut n_blue = u8::MIN;

    for draw in draws {
        n_red = cmp::max(n_red, draw.0);
        n_green = cmp::max(n_green, draw.1);
        n_blue = cmp::max(n_blue, draw.2);
    }

    [n_red, n_green, n_blue]
}

fn solution_p2(input: String) -> u32 {
    let mut total: u32 = 0;
    for line in input.lines() {
        
        let draws = line.split(":").last().expect("Game line should include a colon.")
            .split(";").map(parse_game);

        total += min_cubes(draws).iter().fold(1, |acc, n| acc * (*n as u32));
    }

    total
}


#[cfg(test)]
mod tests {
    use crate::day2::{solution_p1, solution_p2};

    const EXAMPLE: &str = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 8);
    }

    #[test]
    fn pt2() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p2(input), 2286);
    }
}
