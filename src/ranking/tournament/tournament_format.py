from __future__ import annotations

import dataclasses as dc
from typing import Generic, Hashable, Iterable, List, Optional, TypeVar

import pandas as pd
import pandas.io.formats.style as pstyle

from ranking.tournament.duel_score import DuelScore
from ranking.tournament.tournament import Tournament

Side = TypeVar("Side", bound=Hashable)


@dc.dataclass(frozen=True)
class TournamentFormat:
    """
    Formatter for pretty-printing Tournament tables. The table is rendered as a Pandas
    dataframe with styling, for displaying in a notebook.
    """

    win_colour: str = "#dcffdc"
    loss_colour: str = "#ffeeee"
    tie_colour: str = "#fffde7"
    violating_win_colour: str = "#c8e9c8"
    violating_loss_colour: str = "#ffcdd2"
    score_text_colour: str = "#000000"

    diagonal_colour: str = "#b7b7b7"
    diagonal_text_colour: str = "#ffffff"
    diagonal_text_length: int = 3

    index_text_colour: str = "#000088"
    show_column_headers: bool = True
    show_match_results: bool = True
    show_total_scores: bool = True

    def format(
        self, tournament: Tournament[Side], sides: Optional[Iterable[Side]] = None
    ) -> pstyle.Styler:
        if sides is None:
            sides = tournament.sides
        state = _TournamentFormatState(sides)

        for lhs in sides:
            state = self._set_diagonal_entry(state, lhs)
            for rhs in sides:
                if lhs != rhs:
                    score = tournament.score_or_zero(lhs, rhs)
                    state = self._set_off_diagonal_entry(state, lhs, rhs, score)

        state.content_df.columns = list(range(1, 1 + len(state.content_df.columns)))

        state = self._add_match_results(tournament, state)

        return self._apply_style(state)

    def _add_match_results(
        self, tournament: Tournament[Side], state: _TournamentFormatState[Side]
    ) -> _TournamentFormatState[Side]:
        if self.show_match_results:
            scores: List[DuelScore] = [
                tournament.match_results(side) for side in state.content_df.index
            ]
            state = self._add_score_cols(state, scores, "M", "MD")

        if self.show_total_scores:
            scores: List[DuelScore] = [
                tournament.total_score(side) for side in state.content_df.index
            ]
            state = self._add_score_cols(state, scores, "T", "TD")

        return state

    def _add_score_cols(
        self,
        state: _TournamentFormatState[Side],
        scores: List[DuelScore],
        score_col: str,
        score_diff_col: str,
    ) -> _TournamentFormatState[Side]:
        state.content_df[score_col] = scores
        state.css_classes_df[score_col] = ""

        def score_diff(score: DuelScore) -> str:
            if score.lhs == score.rhs:
                return "="
            else:
                return f"{score.lhs - score.rhs:+}"

        state.content_df[score_diff_col] = [score_diff(score) for score in scores]
        state.css_classes_df[score_diff_col] = ""

        return state

    def _apply_style(self, state: _TournamentFormatState[Side]) -> pstyle.Styler:
        state.css_classes_df.columns = state.content_df.columns

        styler: pstyle.Styler = state.content_df.style.set_td_classes(
            state.css_classes_df
        )

        styler = styler.set_table_styles(
            [
                # base cell styling
                {
                    "selector": "td",
                    "props": [
                        ("text-align", "center"),
                        ("border", "2px solid #ffffff"),
                    ],
                },
                # header styling
                {
                    "selector": "th.col_heading",
                    "props": [
                        ("text-align", "center"),
                        ("border", "2px solid #e6e6e6"),
                        ("background-color", "#fafafa"),
                        ("color", self.index_text_colour),
                    ],
                },
                {
                    "selector": "th.row_heading",
                    "props": [
                        ("text-align", "left"),
                        ("border", "2px solid #e6e6e6"),
                        ("background-color", "#fafafa"),
                        ("color", self.index_text_colour),
                    ],
                },
                # per-class cell colours
                {
                    "selector": "td.win",
                    "props": [
                        ("background-color", self.win_colour),
                        ("color", self.score_text_colour),
                    ],
                },
                {
                    "selector": "td.violating_win",
                    "props": [
                        ("background-color", self.violating_win_colour),
                        ("color", self.score_text_colour),
                    ],
                },
                {
                    "selector": "td.loss",
                    "props": [
                        ("background-color", self.loss_colour),
                        ("color", self.score_text_colour),
                    ],
                },
                {
                    "selector": "td.violating_loss",
                    "props": [
                        ("background-color", self.violating_loss_colour),
                        ("color", self.score_text_colour),
                    ],
                },
                {
                    "selector": "td.tie",
                    "props": [
                        ("background-color", self.tie_colour),
                        ("color", self.score_text_colour),
                    ],
                },
                {
                    "selector": "td.diag",
                    "props": [
                        ("background-color", self.diagonal_colour),
                        ("color", self.diagonal_text_colour),
                    ],
                },
            ]
        )

        if not self.show_column_headers:
            styler = styler.set_table_styles(
                [
                    {"selector": "thead", "props": [("display", "none")]},
                    {"selector": "th.blank", "props": [("display", "none")]},
                ],
                overwrite=False,
            )

        return styler

    def _set_diagonal_entry(
        self, state: _TournamentFormatState[Side], side: Side
    ) -> _TournamentFormatState[Side]:
        try:
            row = state.side_idx[side]
            state.content_df.iloc[row, row] = state.label(side)[
                : self.diagonal_text_length
            ]
            state.css_classes_df.iloc[row, row] = "diag"
        except KeyError:
            pass
        return state

    def _set_off_diagonal_entry(
        self,
        state: _TournamentFormatState[Side],
        lhs: Side,
        rhs: Side,
        score: DuelScore,
    ) -> _TournamentFormatState[Side]:
        try:
            row = state.side_idx[lhs]
            col = state.side_idx[rhs]
        except KeyError:
            return state

        state.content_df.iloc[row, col] = str(score)

        if score.lhs > score.rhs:
            cls = "win" if row < col else "violating_win"
        elif score.lhs < score.rhs:
            cls = "loss" if row > col else "violating_loss"
        else:
            cls = "tie"
        state.css_classes_df.iloc[row, col] = cls

        return state


class _TournamentFormatState(Generic[Side]):
    def __init__(self, sides: Iterable[Side]) -> None:
        self.sides_ordered = tuple(sides)
        self.side_idx = {side: idx for idx, side in enumerate(self.sides_ordered)}
        index = [self.label(side) for side in self.sides_ordered]
        self.content_df = pd.DataFrame(index=index, columns=index)
        self.css_classes_df = pd.DataFrame("", index=index, columns=index, dtype=object)

    def label(self, side: Side) -> str:
        return str(side)
