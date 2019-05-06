##############################################################################
#
# ACKNOWLEDGEMENT
#   The code in this module has been copied from the following source:
#     https://github.com/mitchellspryn/QLearningMazeSolver/blob/master/maze.py
#
#   Apart from trimming the code a little bit to serve our purpose for this
#   assignment, we have not made any changes to the original source
#
##############################################################################

import numpy as np

class Paint:
    def __init__(self, maze, goal, start = None, path = None):
        self.maze = maze
        self.path = path
        self.end_point = goal
        self.start_point = start
        
        # CONSTANTS
        self.block_size = 49
        self.WALL_COLOR = [0,0,0]
        self.PATH_COLOR = [127, 127, 127]
        self.GOAL_COLOR = [0, 255, 0]
        self.START_COLOR = [255, 0, 0]
        self.BACKGROUND_COLOR_INT = 255
        self.BACKGROUND_COLOR = [self.BACKGROUND_COLOR_INT for i in range(0, 3, 1)]

    def generate_image(self):
        image = self.__initialize_image()

        if (self.path is not None):
            image = self.__draw_path(image, self.path)
        if (self.start_point is not None):
            image = self.__draw_start(image, self.start_point)
        if (self.end_point is not None):
            image = self.__draw_end(image, self.end_point)

        image = self.__draw_all_walls(image)
        
        for y in range(0, len(self.maze), 1):
            for x in range(0, len(self.maze[0]), 1):
                if (x != 0 or y != 0):
                    image = self.__remove_walls(image, (y,x), self.maze[y][x])
        
        return image

    def __initialize_image(self):
        image = np.full((len(self.maze) * self.block_size, len(self.maze[0]) * self.block_size, 3), self.BACKGROUND_COLOR_INT, dtype=np.uint8)
        return image

    def __draw_all_walls(self, image):
        for y in range(0, image.shape[0], 1):
            for x in range(0, image.shape[1], 1):
                is_wall = False
                if y % self.block_size == 0 or y % self.block_size == self.block_size-1:
                    is_wall = True
                elif x % self.block_size == 0 or x % self.block_size == self.block_size-1:
                    is_wall = True
                if is_wall:
                    image[y][x] = self.WALL_COLOR
        return image

    def __remove_walls(self, image, first_point, second_point):
        if (first_point[0] == second_point[0] and first_point[1] == second_point[1]):
            raise ValueError('Duplicate points: {0} and {1}'.format(first_point, second_point))

        if (first_point[0] == second_point[0]):
            if (first_point[1] > second_point[1]):
                image = self.__remove_left_wall(image, first_point)
                image = self.__remove_right_wall(image, second_point)
            elif (first_point[1] < second_point[1]):
                image = self.__remove_right_wall(image, first_point)
                image = self.__remove_left_wall(image, second_point)
        elif (first_point[1] == second_point[1]):
            if (first_point[0] > second_point[0]):
                image = self.__remove_top_wall(image, first_point)
                image = self.__remove_bottom_wall(image, second_point)
            elif (first_point[0] < second_point[0]):
                image = self.__remove_bottom_wall(image, first_point)
                image = self.__remove_top_wall(image, second_point)
        else:
            raise ValueError('points {0} and {1} cannot be connected.'.format(first_point, second_point))
        return image

    def __remove_top_wall(self, image, point):
        y_px = (point[0]) * self.block_size
        x_start = (point[1] * self.block_size) + 1
        x_end = ( (point[1]+1) * self.block_size ) - 1

        color = self.BACKGROUND_COLOR
        if self.path is not None and point in self.path:
            color = self.PATH_COLOR

        while x_start < x_end:
            image[y_px][x_start] = color
            x_start += 1
        return image

    def __remove_bottom_wall(self, image, point):
        y_px = ((point[0]+1) * self.block_size) - 1
        x_start = (point[1] * self.block_size) + 1
        x_end = ((point[1]+1) * self.block_size) - 1

        color = self.BACKGROUND_COLOR
        if self.path is not None and point in self.path:
            color = self.PATH_COLOR

        while x_start < x_end:
            image[y_px][x_start] = color
            x_start += 1
        return image

    def __remove_left_wall(self, image, point):
        x_px = (point[1]) * self.block_size
        y_start = (point[0] * self.block_size) + 1
        y_end = ( (point[0]+1) * self.block_size ) - 1
        
        color = self.BACKGROUND_COLOR
        if self.path is not None and point in self.path:
            color = self.PATH_COLOR

        while y_start < y_end:
            image[y_start][x_px] = color
            y_start += 1
        return image

    def __remove_right_wall(self, image, point):
        x_px = ((point[1] + 1) * self.block_size) - 1
        y_start = (point[0] * self.block_size) + 1
        y_end = ((point[0]+1) * self.block_size) - 1

        color = self.BACKGROUND_COLOR
        if self.path is not None and point in self.path:
            color = self.PATH_COLOR

        while y_start < y_end:
            image[y_start][x_px] = color
            y_start += 1
        return image
    
    def __draw_start(self, image, point):
        return self.__draw_square_in_center_of_patch(image, point, self.START_COLOR)

    def __draw_end(self, image, point):
        return self.__draw_square_in_center_of_patch(image, point, self.GOAL_COLOR)

    def __draw_square_in_center_of_patch(self, image, point, color):
        center_y_pixel = (point[0] * self.block_size) + (self.block_size // 2)
        center_x_pixel = (point[1] * self.block_size) + (self.block_size // 2)

        min_x = center_x_pixel - 3
        max_x = center_x_pixel + 3
        min_y = center_y_pixel - 3
        max_y = center_y_pixel + 3
        
        return self.__draw_filled_rectangle(image, min_x, min_y, max_x, max_y, color)

    def __draw_path(self, image, path):
        for path_node in path:
            min_x = path_node[1] * self.block_size
            min_y = path_node[0] * self.block_size
            max_x = (path_node[1] + 1) * self.block_size
            max_y = (path_node[0] + 1) * self.block_size

            image = self.__draw_filled_rectangle(image, min_x, min_y, max_x, max_y, self.PATH_COLOR)

        return image

    def __draw_filled_rectangle(self, image, min_x, min_y, max_x, max_y, color):
        for y in range(min_y, max_y, 1):
            for x in range(min_x, max_x, 1):
                image[y][x] = color
        return image