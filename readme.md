# WAR - our version of the card game

How often does a battle result in a war -- a simulation...

## General rules

Play the game of war with the "staking rules" as follows

- to battle: stake a card and play a card
- if there's a winner (one card's value is greater than the other), the winner of the battle takes the opponents battle card
- if there's a war (card values are equal, or one is a joker), stake 3 cards and play another battle
  -- if there a winner, the winner takes all opponents staked cards
- repeat until one player runs out of cards.

## End of game nuance

- if a player can't stake 3 cards for a war from cards in hand:
  -- pick up any winnings from previous battles and continue playing
  -- if the player still can't meet the battle stakes, simply play the last card and hope for a win

## War odds?

This simulator will play games according to these rules and track how many
battles were fought and how many resulted in a war and chart the results.
