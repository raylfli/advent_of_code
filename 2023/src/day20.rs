use num::integer::lcm;
use std::collections::{HashMap, VecDeque};

use itertools::Itertools;

pub fn solution(input: String, part2: bool) {
    if part2 {
        println!("{}", solution_p2(input));
    } else {
        println!("{}", solution_p1(input));
    }
}

enum CommModule {
    Broadcast,
    FlipFlop,
    Conjunction,
}

/// Parse input
fn parse_input<'a>(input: &'a String) -> HashMap<&'a str, (CommModule, HashMap<&'a str, bool>, Vec<&'a str>, bool)> {

    // find neighbours
    let mut neighbours: HashMap<&str, Vec<&str>> = HashMap::new(); // neighbours
    for line in (*input).lines() {
        let (label, conn_str) = line.split(" -> ").collect_tuple().expect("Must have two parts.");
        let dests = conn_str.split(", ").collect_vec();
        let label_trimmed = if label.starts_with('%') || label.starts_with('&') {
            &label[1..]
        } else {
            label
        };
        for dest in dests {
            let dest_trimmed = if dest.starts_with('%') || dest.starts_with('&') {
                &dest[1..]
            } else {
                dest
            };
            if neighbours.contains_key(dest_trimmed) {
                neighbours.get_mut(dest_trimmed).unwrap().push(label_trimmed);
            } else {
                neighbours.insert(dest_trimmed, vec![label_trimmed]);
            }
        }
        
    }

    // create all modules
    let mut modules: HashMap<&'a str, (CommModule, HashMap<&'a str, bool>, Vec<&'a str>, bool)> = HashMap::new();
    for line in (*input).lines() {
        let (label, conn_str) = line.split(" -> ").collect_tuple().expect("Must have two parts.");
        let dests = conn_str.split(", ").collect_vec();
        if label.starts_with('%') {
            modules.insert(&label[1..], (
                CommModule::FlipFlop,
                HashMap::new(), // no need for input mapping
                dests,
                false
            ));
        } else if label.starts_with('&') {
            modules.insert(&label[1..], (
                CommModule::Conjunction,
                neighbours
                    .get(&label[1..])
                    .expect("Must have matching input label.")
                    .into_iter()
                    .map(|inp| (*inp, false))
                    .collect::<HashMap<&str, bool>>(),
                dests,
                false
            ));
        } else {
            modules.insert(label, (
                CommModule::Broadcast,
                HashMap::new(), // no need for input mapping
                dests,
                false
            ));
        }
    }

    modules

}

fn solution_p1(input: String) -> usize {

    let mut modules = parse_input(&input);

    let mut cycle_low: Vec<usize> = vec![];
    let mut cycle_high: Vec<usize> = vec![];
    let mut i = 0_usize;

    while i < 1000 && (i == 0 || modules.iter().any(
        |(_label, (_mod_type, inputs, _outputs, state))|
        {
            *state || inputs.values().any(|b| *b)
        }
    )) {
        let mut messages: VecDeque<(&str, &str, bool)> = VecDeque::from([("", "broadcaster", false)]);
        cycle_high.push(0);
        cycle_low.push(0);
        while messages.len() > 0 {
            let (from, to, ptype) = messages.pop_front().unwrap();
            if ptype {
                cycle_high[i] += 1;
            } else {
                cycle_low[i] += 1;
            }
    
            if !modules.contains_key(to) {
                continue;
            }
    
            let module = modules
                .get_mut(to)
                .unwrap();
            let (to_type, to_inputs, to_outputs, to_state) = module;
            
            match to_type {
                CommModule::Broadcast => {
                    let new_messages = to_outputs
                        .iter()
                        .map(|out| (to, *out, *to_state));
                    messages.extend(new_messages);
                },
                CommModule::FlipFlop => {
                    if !ptype {
                        *to_state = !*to_state;
                        let new_messages = to_outputs
                            .iter()
                            .map(|out| (to, *out, *to_state));
                        messages.extend(new_messages);
                    }
                },
                CommModule::Conjunction => {
                    let from_last_pulse = to_inputs.get_mut(from).expect("Must be valid input connection.");
                    *from_last_pulse = ptype;
                    let out_pulse = if to_inputs.values().all(|b| *b) { false } else { true };
                    let new_messages = to_outputs
                            .iter()
                            .map(|out| (to, *out, out_pulse));
                    messages.extend(new_messages);
                },
            }
        }
        i += 1;
    }

    if i == 1000 {
        return cycle_low.iter().sum::<usize>() * cycle_high.iter().sum::<usize>();
    }

    let cycle_len = cycle_low.len();
    let total_cycle_low = cycle_low.iter().sum::<usize>();
    let total_cycle_high = cycle_high.iter().sum::<usize>();

    let num_cycles = 1000 / cycle_len;
    let rem_cycles = 1000 % cycle_len;

    let low_pulses = total_cycle_low * num_cycles + cycle_low[..rem_cycles].iter().sum::<usize>();
    let high_pulses = total_cycle_high * num_cycles + cycle_high[..rem_cycles].iter().sum::<usize>();

    low_pulses * high_pulses

}

fn solution_p2(input: String) -> usize {

    let mut modules = parse_input(&input);
    let mut presses = 0_usize;

    let pre_rx_conj = "tj"; // from input inspection
    let pre_rx_n_inputs = (*modules
        .get(pre_rx_conj)
        .expect("Must have pre_rx conjunction input.")
    ).1.len();
    let mut pre_rx_cycles: HashMap<&str, usize> = HashMap::new();

    while pre_rx_cycles.len() != pre_rx_n_inputs {
        let mut messages: VecDeque<(&str, &str, bool)> = VecDeque::from([("", "broadcaster", false)]);
        presses += 1;
        while messages.len() > 0 {
            let (from, to, ptype) = messages.pop_front().unwrap();
    
            if !modules.contains_key(to) {
                continue;
            }
    
            let module = modules
                .get_mut(to)
                .unwrap();
            let (to_type, to_inputs, to_outputs, to_state) = module;
            
            match to_type {
                CommModule::Broadcast => {
                    let new_messages = to_outputs
                        .iter()
                        .map(|out| (to, *out, *to_state));
                    messages.extend(new_messages);
                },
                CommModule::FlipFlop => {
                    if !ptype {
                        *to_state = !*to_state;
                        let new_messages = to_outputs
                            .iter()
                            .map(|out| (to, *out, *to_state));
                        messages.extend(new_messages);
                    }
                },
                CommModule::Conjunction => {
                    if ptype && to == pre_rx_conj && !pre_rx_cycles.contains_key(to) {
                        pre_rx_cycles.insert(from, presses);
                    }

                    let from_last_pulse = to_inputs.get_mut(from).expect("Must be valid input connection.");
                    *from_last_pulse = ptype;
                    let out_pulse = if to_inputs.values().all(|b| *b) { false } else { true };
                    let new_messages = to_outputs
                            .iter()
                            .map(|out| (to, *out, out_pulse));
                    messages.extend(new_messages);
                },
            }
        }
    }

    pre_rx_cycles
        .into_values()
        .reduce(lcm)
        .expect("Must have at least one pre-rx input.")

}


#[cfg(test)]
mod tests {
    use crate::day20::solution_p1;

    const EXAMPLE: &str = "broadcaster -> a, b, c\n%a -> b\n%b -> c\n%c -> inv\n&inv -> a\n";
    const EXAMPLE2: &str = "broadcaster -> a\n%a -> inv, con\n&inv -> b\n%b -> con\n&con -> output\n";

    #[test]
    fn pt1() {
        let input = String::from(EXAMPLE);
        assert_eq!(solution_p1(input), 32000000);
    }

    #[test]
    fn pt1_2() {
        let input = String::from(EXAMPLE2);
        assert_eq!(solution_p1(input), 11687500);
    }

}
