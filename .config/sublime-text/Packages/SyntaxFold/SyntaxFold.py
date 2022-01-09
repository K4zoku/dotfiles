import os
import shutil
import sublime
import sublime_plugin

def plugin_loaded():
    user_settings_path = os.path.join(
        sublime.packages_path(),
        "User",
        "syntax_fold.sublime-settings")

    if not os.path.exists(user_settings_path):
        default_settings_path = os.path.join(
            sublime.packages_path(),
            "SyntaxFold",
            "syntax_fold.sublime-settings")

        shutil.copyfile(default_settings_path, user_settings_path)


def get_source_scope(view):
    all_scopes = view.scope_name(view.sel()[0].begin())
    split_scopes = all_scopes.split(" ")
    for scope in split_scopes:
        if scope.find("source.") != -1  or \
         scope.find("embedding.") != -1 or \
         scope.find("text.") != -1:
            return scope
    return None


def get_markers(view):
    source_scope = get_source_scope(view)
    if source_scope is None:
        print("SyntaxFold: No source scope was found. ")
        return None, None

    settings = sublime.load_settings("syntax_fold.sublime-settings")
    configs = settings.get("config")
    start_marker = None
    end_marker = None
    marker_pairs = []
    for config_object in configs:
        config_scope = config_object.get("scope", "")

        # allow for comma seperated source specifications
        if source_scope in config_scope:
            start_marker = config_object.get("startMarker", None)
            end_marker = config_object.get("endMarker", None)
            marker_pairs.append((start_marker,end_marker))

    return marker_pairs


def get_all_positions(view,marker_pair):

    start_marker, end_marker = marker_pair
    if start_marker is None:
        print("SyntaxFold: At least start marker must be specified. "
              "Aborting request.")
        return None, None

    start_positions = []
    end_positions = []

    # fill start positions
    start_markers = view.find_all(start_marker)
    for marker in start_markers:
        start_positions.append(view.line(marker.end()).end())

    # fill end positions
    if end_marker is not None:
        end_markers = view.find_all(end_marker)
        for marker in end_markers:
            end_positions.append(view.line(marker.begin()).begin()-1)

    # If no end marker specified
    # utilize the next start marker as the end position
    else:
        for index in range(0, len(start_positions)-1):
            end_positions.append(view.line(start_positions[index+1]).begin()-1)
        end_positions.append(view.size())

    end_positions_len = len(end_positions)
    start_positions_len = len(start_positions)

    if start_positions_len == 0 and end_positions_len == 0:
        print("SyntaxFold: No start markers or end markers found for: \n Start marker: \""+start_marker+"\" and end marker: \""+end_marker+"\"\n Skipping marker entry")
        return None, None

    return start_positions, end_positions


def get_all_fold_regions(view):

    regions = []
    for marker_pair in get_markers(view):
        start_positions, end_positions = get_all_positions(view,marker_pair)

        last_matched_end_pos = -1
        if start_positions is None or end_positions is None:
            continue

        for end_pos in end_positions:
            last_matched_start_pos = -1
            for start_pos in start_positions:

                # if the start pos is beyond the position of
                # the end pos it isn"t a match
                if start_pos > end_pos:
                    break

                # The start pos must be greater or equal to then the
                # last matched end post when matching
                elif start_pos > last_matched_end_pos:
                    last_matched_start_pos = start_pos

            if last_matched_start_pos != -1:
                start_match_position = view.line(last_matched_start_pos-1).begin()
                end_match_position = view.line(end_pos+1).end()
                last_matched_end_pos = end_pos
                regions.append((
                    last_matched_start_pos,
                    end_pos,
                    start_match_position,
                    end_match_position))

    if len(regions) == 0:
        return None

    return regions


def operation_on_all_regions(fold_regions, operation):

    regions = []
    for fold_region in fold_regions:
        regions.append(sublime.Region(fold_region[0], fold_region[1]))

    operation(regions)


def operation_on_selected_region(selection, fold_regions, operation):

    for fold_region in fold_regions:
        if (fold_region[2] <= selection.begin()
                and fold_region[3] >= selection.end()):
            content = [sublime.Region(fold_region[0], fold_region[1])]
            operation(content)
            break


#
# Operations
#
class FoldCommands(sublime_plugin.TextCommand):

    def fold(self, regions):
        if len(regions) > 0:
            self.view.fold(regions)

    def unfold(self, regions):
        if len(regions) > 0:
            self.view.unfold(regions)


class SyntaxfoldFoldAllCommand(FoldCommands):
    def run(self, edit):
        fold_regions = get_all_fold_regions(self.view)
        if fold_regions is None:
            return

        operation_on_all_regions(fold_regions, self.fold)


class SyntaxfoldUnfoldAllCommand(FoldCommands):
    def run(self, edit):
        fold_regions = get_all_fold_regions(self.view)
        if fold_regions is None:
            return

        operation_on_all_regions(fold_regions, self.unfold)


class SyntaxfoldToggleFoldCurrentCommand(FoldCommands):
    def run(self, edit):
        fold_regions = get_all_fold_regions(self.view)
        if fold_regions is None:
            return

        selection = self.view.sel()[0]

        if self.view.is_folded(selection):
            operation_on_selected_region(selection, fold_regions, self.unfold)
        else:
            operation_on_selected_region(selection, fold_regions, self.fold)