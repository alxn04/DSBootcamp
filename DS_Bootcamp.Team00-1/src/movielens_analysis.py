from collections import Counter, defaultdict
from datetime import datetime

import pytest
import requests
from bs4 import BeautifulSoup


def read_csv(path_to_the_file, count_rows, is_dict=True):
    if is_dict:
        data = dict()
    else:
        data = list()
    try:
        with open(path_to_the_file, "r") as movie:
            movie.readline()
            for _ in range(count_rows):
                line = movie.readline()
                split_line = []
                line_item = ""
                is_quote = -1
                for letter in line:
                    if letter == "," and is_quote == -1:
                        split_line.append(line_item)
                        line_item = ""
                    elif letter == '"':
                        is_quote *= -1
                    else:
                        line_item += letter
                split_line.append(line_item[:-1])
                if is_dict:
                    data[split_line[0]] = split_line[1:]
                else:
                    data.append(split_line)
    except FileNotFoundError:
        print(f"Error: The file '{path_to_the_file}' was not found.")
    except IOError as e:
        print(
            f"Error: An I/O error occurred while trying to read the file. Details: {e}"
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
    return data


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file, count_rows=1000):
        self.data = read_csv(path_to_the_file, count_rows)
        self.genres_list = [
            "Action",
            "Adventure",
            "Animation",
            "Children",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Fantasy",
            "Film-Noir",
            "Horror",
            "Musical",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Thriller",
            "War",
            "Western",
            "(no genres listed)",
        ]

    def dist_by_release(self):
        years_list = []
        for line in self.data.values():
            if line[0].endswith(")"):
                year = line[0][-5:].strip(")")
                years_list.append(year)
        release_years = dict(
            sorted(Counter(years_list).items(), key=lambda item: item[1], reverse=True)
        )
        return release_years

    def dist_by_genres(self):
        genres = []
        for line in self.data.values():
            for genre in line[1].split("|"):
                if genre in self.genres_list:
                    genres.append(genre)
        return dict(
            sorted(Counter(genres).items(), key=lambda item: item[1], reverse=True)
        )

    def most_genres(self, n):
        genres = Counter(self.dist_by_genres())
        return dict(genres.most_common(n))

    def movies_with_word(self, word):
        unique_movies = {
            movie[0] for movie in self.data.values() if word.lower() in movie[0].lower()
        }
        return sorted(unique_movies)


class Links:
    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file, count_rows=20):
        self.filepath = path_to_the_file
        self.data = read_csv(self.filepath, count_rows)
        self.imdb_info = self.get_imdb(
            self.data,
            ["Director", "Budget", "Gross worldwide", "Runtime", "Stars", "Title"],
        )

    @staticmethod
    def get_imdb(list_of_movies, list_of_fields):
        imdb_info = []
        imdbId = [line[0] for line in list_of_movies.values()]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        for movie_id in imdbId:
            try:
                imdb_url = f"https://www.imdb.com/title/tt{movie_id}/"
                response = requests.get(imdb_url, headers=headers)
                response.raise_for_status
                soup = BeautifulSoup(response.text, "html.parser")

                movie_data = [movie_id]
                for field in list_of_fields:
                    field_tag = soup.find(string=field)
                    if field == "Writers":
                        item_string = (
                            ", ".join(
                                a.text.strip()
                                for a in field_tag.find_next("div").find_all("a")
                            )
                            if field_tag
                            else "n/a"
                        )
                    elif field == "Director" and field_tag == None:
                        field_tag = soup.find(string="Directors")
                        item_string = (
                            field_tag.find_next("div").find_next("a").text.strip()
                            if field_tag
                            else None
                        )
                    elif field in {"Director", "Stars"}:
                        item_string = (
                            field_tag.find_next("a").text.strip() if field_tag else None
                        )
                    elif field == "Title":
                        field_tag = soup.find(class_="hero__primary-text")
                        item_string = field_tag.text.strip() if field_tag else None
                    else:
                        item_string = (
                            field_tag.find_next().text.strip() if field_tag else "n/a"
                        )

                    movie_data.append(item_string)
                imdb_info.append(movie_data)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к IMDb для фильма {movie_id}: {e}")

        return imdb_info

    @staticmethod
    def sort_dict_top_n(movie_dict, n):
        sorted_dict = dict(sorted(movie_dict.items(), key=lambda x: x[1], reverse=True))
        return dict(list(sorted_dict.items())[:n])

    @staticmethod
    def clean_budget(budget_str):
        clean = ""
        for symbol in budget_str:
            if symbol >= "0" and symbol <= "9":
                clean += symbol
        return clean.lstrip("0")

    @staticmethod
    def clean_time(time_str):
        time_arr = time_str.split()
        hour_to_min = int(time_arr[0]) * 60
        total_min = hour_to_min + int(time_arr[2])
        return total_min

    def top_directors(self, n):
        list_of_directors = [item[1] for item in self.imdb_info]
        directors_dict = Counter(list_of_directors)
        directors = directors_dict.most_common(n)
        return dict(directors)

    def most_expensive(self, n):
        movie_dict = {
            movie[-1]: int(self.clean_budget(movie[2]))
            for movie in self.imdb_info
            if self.clean_budget(movie[2]) != ""
        }
        budgets = self.sort_dict_top_n(movie_dict, n)

        return budgets

    def most_profitable(self, n):
        movie_dict = {
            movie[-1]: (
                int(self.clean_budget(movie[3])) - int(self.clean_budget(movie[2]))
            )
            for movie in self.imdb_info
            if self.clean_budget(movie[2]) != "" and self.clean_budget(movie[3]) != ""
        }
        profits = self.sort_dict_top_n(movie_dict, n)
        return profits

    def longest(self, n):
        movie_dict = {
            movie[-1]: f"{self.clean_time(movie[4])} min" for movie in self.imdb_info
        }
        runtimes = self.sort_dict_top_n(movie_dict, n)
        return runtimes

    def top_cost_per_minute(self, n):
        movie_dict = {
            movie[-1]: round(
                (int(self.clean_budget(movie[2])) / int(self.clean_time(movie[4]))), 2
            )
            for movie in self.imdb_info
            if self.clean_budget(movie[2]) != ""
        }
        costs = self.sort_dict_top_n(movie_dict, n)
        return costs

    def top_stars(self, n):
        list_of_stars = [item[-2] for item in self.imdb_info]
        stars_dict = Counter(list_of_stars)
        stars = stars_dict.most_common(n)
        return dict(stars)


class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file, count_rows=1000):
        self.data = read_csv(path_to_the_file, count_rows, False)
        self.list_of_tags = [item[2] for item in self.data]
        self.unique_tags = set(self.list_of_tags)

    def most_words(self, n):
        tag_word_counts = {tag: len(tag.split()) for tag in self.unique_tags}
        sorted_tags = sorted(tag_word_counts.items(), key=lambda x: x[1], reverse=True)
        big_tags = dict(sorted_tags[:n])
        return big_tags

    def longest(self, n):
        sorted_tags = sorted(self.unique_tags, key=len, reverse=True)
        big_tags = sorted_tags[:n]
        return big_tags

    def most_words_and_longest(self, n):
        most_words = self.most_words(n)
        longest = self.longest(n)
        big_tags = list(set(most_words.keys()) & set(longest))
        return big_tags

    def most_popular(self, n):
        tag_counts = Counter(self.list_of_tags)
        popular_tags = dict(
            list(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True))[:10]
        )

        return popular_tags

    def tags_with(self, word):
        filtered_tags = [tag for tag in self.unique_tags if word in tag]
        tags_with_word = sorted(filtered_tags)
        return tags_with_word


class Ratings:
    def __init__(self, path_to_the_file, count_rows=1000):
        self.data = read_csv(path_to_the_file, count_rows, False)

    class Movies:
        def __init__(self, data, movie_data):
            self.data = data
            self.movie_data = movie_data

        def get_movie_title(self, movie_id):
            return self.movie_data[str(movie_id)][0]

        def dist_by_year(self):
            year_counts = Counter(
                [datetime.fromtimestamp(int(row[3])).year for row in self.data]
            )
            ratings_by_year = dict(
                sorted(year_counts.items(), key=lambda item: item[1])
            )
            return ratings_by_year

        def dist_by_rating(self):
            ratings_counts = {}
            for row in self.data:
                rating = float(row[2])
                if rating in ratings_counts:
                    ratings_counts[rating] += 1
                else:
                    ratings_counts[rating] = 1

            ratings_distribution = dict(
                sorted(ratings_counts.items(), key=lambda item: item[1])
            )
            return ratings_distribution

        def top_by_num_of_ratings(self, n):
            movie_ratings_count = {}
            for row in self.data:
                movie_id = row[1]
                movie_title = self.get_movie_title(movie_id)
                if movie_title in movie_ratings_count:
                    movie_ratings_count[movie_title] += 1
                else:
                    movie_ratings_count[movie_title] = 1

            sorted_movies = dict(
                sorted(
                    movie_ratings_count.items(), key=lambda item: item[1], reverse=True
                )
            )
            top_movies = dict(list(sorted_movies.items())[:n])
            return top_movies

        def top_by_ratings(self, n, metric="average"):
            movie_ratings = defaultdict(list)
            for row in self.data:
                movie_id = row[1]
                movie_title = self.get_movie_title(movie_id)
                rating = float(row[2])
                movie_ratings[movie_title].append(rating)

            if metric == "average":
                metric_func = lambda ratings: sum(ratings) / len(ratings)
            elif metric == "median":
                metric_func = lambda ratings: sorted(ratings)[len(ratings) // 2]
            else:
                raise ValueError("Metric must be 'average' or 'median'")

            movie_metrics = {
                movie: round(metric_func(ratings), 2)
                for movie, ratings in movie_ratings.items()
            }
            top_movies = dict(
                sorted(movie_metrics.items(), key=lambda x: x[1], reverse=True)[:n]
            )
            return top_movies

        def top_controversial(self, n):
            movie_ratings = defaultdict(list)
            for row in self.data:
                movie_id = row[1]
                movie_title = self.get_movie_title(movie_id)
                rating = float(row[2])
                movie_ratings[movie_title].append(rating)

            movie_variances = {}
            for movie, ratings in movie_ratings.items():
                if len(ratings) < 2:
                    movie_variances[movie] = 0
                    continue

                mean = sum(ratings) / len(ratings)
                variance = sum([(x - mean) ** 2 for x in ratings]) / (len(ratings) - 1)
                movie_variances[movie] = round(variance, 2)

            top_movies = dict(
                sorted(movie_variances.items(), key=lambda item: item[1], reverse=True)[
                    :n
                ]
            )
            return top_movies

    class Users(Movies):
        def dist_by_num_of_ratings(self):
            user_ratings_count = {}
            for row in self.data:
                user_id = row[0]
                if user_id in user_ratings_count:
                    user_ratings_count[user_id] += 1
                else:
                    user_ratings_count[user_id] = 1

            sorted_users = dict(
                sorted(
                    user_ratings_count.items(), key=lambda item: item[1], reverse=True
                )
            )
            return sorted_users

        def dist_by_ratings(self, metric="average"):
            user_ratings = defaultdict(list)
            for row in self.data:
                user_id = row[0]
                rating = float(row[2])
                user_ratings[user_id].append(rating)

            if metric == "average":
                metric_func = lambda ratings: (
                    sum(ratings) / len(ratings) if ratings else 0
                )
            elif metric == "median":
                metric_func = lambda ratings: (
                    sorted(ratings)[len(ratings) // 2] if ratings else 0
                )
            else:
                raise ValueError("Metric must be 'average' or 'median'")

            user_metrics = {
                user: round(metric_func(ratings), 2)
                for user, ratings in user_ratings.items()
            }
            sorted_users = dict(
                sorted(user_metrics.items(), key=lambda item: item[1], reverse=True)
            )
            return sorted_users

        def top_controversial(self, n):
            user_ratings = defaultdict(list)
            for row in self.data:
                user_id = row[0]
                rating = float(row[2])
                user_ratings[user_id].append(rating)

            user_variances = {}
            for user, ratings in user_ratings.items():
                if len(ratings) < 2:
                    user_variances[user] = 0
                    continue

                mean = sum(ratings) / len(ratings)
                variance = sum([(x - mean) ** 2 for x in ratings]) / (len(ratings) - 1)
                user_variances[user] = round(variance, 2)
            top_users = dict(
                sorted(user_variances.items(), key=lambda item: item[1], reverse=True)[
                    :n
                ]
            )
            return top_users


class Test:
    # Tests should check:
    #     if the methods return the correct data types
    #     if the lists elements have the correct data types
    #     if the returned data sorted correctly

    # Test class Movies
    # Count rows from movies.csv : 1000
    class TestMovies:
        @pytest.fixture
        def movies(self):
            return Movies("../datasets/movies.csv", 1000)

        def test_load_movies(self, movies):
            assert isinstance(movies.data, dict)
            for movie in movies.data.values():
                assert isinstance(movie, list)
                assert len(movie) == 2

        def test_releases(self, movies):
            assert type(movies.dist_by_release()).__name__ == "dict"
            for item in movies.dist_by_release().keys():
                assert type(item).__name__ == "str"
            for item in movies.dist_by_release().values():
                assert type(item).__name__ == "int"
            assert sorted(movies.dist_by_release().values(), reverse=True) == list(
                movies.dist_by_release().values()
            )

        def test_genres(self, movies):
            assert type(movies.dist_by_genres()).__name__ == "dict"
            for item in movies.dist_by_genres().keys():
                assert type(item).__name__ == "str"
            for item in movies.dist_by_genres().values():
                assert type(item).__name__ == "int"
            assert len(movies.dist_by_genres()) == 18
            sorted(movies.dist_by_genres().values(), reverse=True) == list(
                movies.dist_by_genres().values()
            )

        def test_top_genres(self, movies):
            assert type(movies.most_genres(10)).__name__ == "dict"
            assert movies.most_genres(5) == dict(
                {
                    "Drama": 507,
                    "Comedy": 365,
                    "Romance": 208,
                    "Thriller": 179,
                    "Action": 158,
                }
            )
            assert sorted(movies.most_genres(10).values(), reverse=True) == list(
                movies.most_genres(10).values()
            )
            for item in movies.most_genres(5).keys():
                assert type(item).__name__ == "str"
            for item in movies.most_genres(10).values():
                assert type(item).__name__ == "int"

        def test_movie_with_word(self, movies):
            word = "hero"
            result = movies.movies_with_word("hero")
            assert type(result).__name__ == "list"
            for item in result:
                assert type(item).__name__ == "str"
                assert word.lower() in item.lower()

    # Test class Tags
    # Count rows from tags.csv : 1000
    class TestTags:
        @pytest.fixture
        def tags(self):
            return Tags("../datasets/tags.csv", 1000)

        def test_most_words(self, tags):
            result = tags.most_words(10)
            assert isinstance(result, dict)
            for tag, count in result.items():
                assert isinstance(tag, str)
                assert isinstance(count, int)
            assert list(result.values()) == sorted(result.values(), reverse=True)

        def test_longest(self, tags):
            result = tags.longest(10)
            assert isinstance(result, list)
            for i in range(1, len(result)):
                assert isinstance(result[i], str)
                assert len(result[i]) <= len(result[i - 1])
            assert len(result) == len(set(result))
            tag_lengths = [len(tag) for tag in result]
            assert tag_lengths == sorted(tag_lengths, reverse=True)

        def test_most_words_and_longest(self, tags):
            result = tags.most_words_and_longest(10)
            assert isinstance(result, list)
            assert sorted(result) == sorted(list(set(result)))
            for item in result:
                assert isinstance(item, str)

        def test_most_popular(self, tags):
            result = tags.most_popular(10)
            assert isinstance(result, dict)
            assert list(result.values()) == sorted(result.values(), reverse=True)
            for tag, count in result.items():
                assert isinstance(tag, str)
                assert isinstance(count, int)
            assert len(result) <= len(set(result.keys()))

        def test_tags_with(self, tags):
            word = "hero"
            result = tags.tags_with(word)
            assert isinstance(result, list)
            for item in result:
                assert isinstance(item, str)
                assert word.lower() in item.lower()

    # Test class Links
    # Count rows from links.csv : 10
    class TestLinks:
        @pytest.fixture
        def get_links(self):
            return Links("../datasets/links.csv", 10)

        @pytest.fixture
        def n(self):
            return 10

        def test_get_imbd(self, get_links):
            assert (
                type(
                    get_links.get_imdb(
                        get_links.data,
                        ["Director", "Budget", "Gross worldwide", "Runtime", "Title"],
                    )
                ).__name__
                == "list"
            )
            for item in get_links.get_imdb(
                get_links.data,
                ["Director", "Budget", "Gross worldwide", "Runtime", "Title"],
            ):
                assert type(item).__name__ == "list"

        def test_top_directors(self, get_links, n):
            assert type(get_links.top_directors(n)).__name__ == "dict"
            assert all(
                isinstance(key, str) for key in get_links.top_directors(n).keys()
            )
            assert all(
                isinstance(value, int) for value in get_links.top_directors(n).values()
            )
            counts = list(get_links.top_directors(n).values())
            assert counts == sorted(counts, reverse=True)

        def test_most_exspensive(self, get_links, n):
            assert type(get_links.most_expensive(n)).__name__ == "dict"
            assert all(
                isinstance(key, str) for key in get_links.most_expensive(n).keys()
            )
            assert all(
                isinstance(value, int) for value in get_links.most_expensive(n).values()
            )
            summ = list(get_links.most_expensive(n).values())
            assert summ == sorted(summ, reverse=True)

        def test_most_profitable(self, get_links, n):
            assert type(get_links.most_profitable(n)).__name__ == "dict"
            assert all(
                isinstance(key, str) for key in get_links.most_profitable(n).keys()
            )
            assert all(
                isinstance(value, int)
                for value in get_links.most_profitable(n).values()
            )
            profits = list(get_links.most_profitable(n).values())
            assert profits == sorted(profits, reverse=True)

        def test_longest(self, get_links, n):
            assert type(get_links.longest(n)).__name__ == "dict"
            assert all(isinstance(key, str) for key in get_links.longest(n).keys())
            assert all(
                isinstance(value, str) for value in get_links.longest(n).values()
            )
            runtimes = list(get_links.longest(n).values())
            assert runtimes == sorted(runtimes, reverse=True)

        def test_top_cost_per_minute(self, get_links, n):
            assert type(get_links.top_cost_per_minute(n)).__name__ == "dict"
            assert all(
                isinstance(key, str) for key in get_links.top_cost_per_minute(n).keys()
            )
            assert all(
                isinstance(value, float)
                for value in get_links.top_cost_per_minute(n).values()
            )
            costs = list(get_links.top_cost_per_minute(n).values())
            assert costs == sorted(costs, reverse=True)

        def test_top_stars(self, get_links, n):
            assert type(get_links.top_stars(n)).__name__ == "dict"
            assert all(isinstance(key, str) for key in get_links.top_stars(n).keys())
            assert all(
                isinstance(value, int) for value in get_links.top_stars(n).values()
            )
            stars = list(get_links.top_stars(n).values())
            assert stars == sorted(stars, reverse=True)

        def test_sort_dict_top_n(self, get_links, n):
            row_result = {
                "31mil": 31999999,
                "55mil": 55000000,
                "60mil": 60000000,
                "15mil": 15000000,
                "50mil": 50000000,
            }
            expected_result = {
                "60mil": 60000000,
                "55mil": 55000000,
                "50mil": 50000000,
                "31mil": 31999999,
                "15mil": 15000000,
            }
            sorted_dict = get_links.sort_dict_top_n(row_result, n)
            assert type(get_links.sort_dict_top_n(row_result, n)).__name__ == "dict"
            assert list(sorted_dict.keys()) == list(expected_result.keys())
            assert list(sorted_dict.values()) == list(expected_result.values())

        def test_clean_budget(self, get_links):
            row_result = "$3,000,000"
            expected_result = "3000000"
            assert type(get_links.clean_budget(row_result)).__name__ == "str"
            assert get_links.clean_budget(row_result) == expected_result

        def test_clean_time(self, get_links):
            row_result = "1 hour 36 minuts"
            expected_result = 96
            assert type(get_links.clean_time(row_result)).__name__ == "int"
            assert get_links.clean_time(row_result) == expected_result

    # Test class Ratings
    # Count rows from tags.csv : 1000
    class TestRatings:
        @pytest.fixture
        def ratings_fixture(self):
            ratings_fixture = Ratings("../datasets/ratings.csv")
            return ratings_fixture

        @pytest.fixture
        def movies(self, ratings_fixture):
            return Ratings.Movies(
                ratings_fixture.data, Movies("../datasets/movies.csv", 9743).data
            )

        @pytest.fixture
        def users(self, ratings_fixture):
            return Ratings.Users(
                ratings_fixture.data, Movies("../datasets/movies.csv", 9743).data
            )

        def test_load_ratings(self, ratings_fixture):
            ratings = ratings_fixture
            assert isinstance(ratings.data, list), "Data should be a list"

        def test_load_movies(self, movies):
            assert isinstance(
                movies.movie_data, dict
            ), "Movies data should be a dictionary"

        def test_dist_by_year(self, movies):
            result = movies.dist_by_year()
            assert isinstance(result, dict), "Result should be a dictionary"
            assert all(
                isinstance(year, int) for year in result.keys()
            ), "Year should be an integer"
            assert all(
                isinstance(count, int) for count in result.values()
            ), "Count should be an integer"
            sorted_years = sorted(result.values())
            assert (
                list(result.values()) == sorted_years
            ), "Result should be sorted by year"

        def test_dist_by_rating(self, movies):
            result = movies.dist_by_rating()
            assert isinstance(result, dict), "Result should be a dictionary"
            assert all(
                isinstance(rating, float) for rating in result.keys()
            ), "Rating should be a float"
            assert all(
                isinstance(count, int) for count in result.values()
            ), "Count should be an integer"
            sorted_ratings = sorted(result.values())
            assert (
                list(result.values()) == sorted_ratings
            ), "Result should be sorted by rating"

        def test_top_by_num_of_ratings(self, movies):
            result = movies.top_by_num_of_ratings(10)
            assert isinstance(result, dict), "Result should be a dictionary"
            assert all(
                isinstance(title, str) for title in result.keys()
            ), "Movie title should be a string"
            assert all(
                isinstance(count, int) for count in result.values()
            ), "Count should be an integer"
            sorted_by_count = sorted(result.items(), key=lambda x: x[1], reverse=True)
            assert (
                list(result.items()) == sorted_by_count
            ), "Result should be sorted by count descending"

        def test_top_by_ratings(self, movies):
            result = movies.top_by_ratings(10)
            assert isinstance(result, dict), "Result should be a dictionary"
            assert all(
                isinstance(title, str) for title in result.keys()
            ), "Movie title should be a string"
            assert all(
                isinstance(avg_rating, float) for avg_rating in result.values()
            ), "Average rating should be a float"
            sorted_by_rating = sorted(result.items(), key=lambda x: x[1], reverse=True)
            assert (
                list(result.items()) == sorted_by_rating
            ), "Result should be sorted by average rating descending"

        def test_top_controversial(self, movies):
            result = movies.top_controversial(10)
            assert isinstance(result, dict), "Result should be a dictionary"
            assert all(
                isinstance(title, str) for title in result.keys()
            ), "Movie title should be a string"
            assert all(
                isinstance(avg_rating, float) for avg_rating in result.values()
            ), "Variance of rating should be a float"
            sorted_by_rating = sorted(result.items(), key=lambda x: x[1], reverse=True)
            assert (
                list(result.items()) == sorted_by_rating
            ), "Result should be sorted by variance of rating descending"

        def test_dist_by_num_of_ratings(self, users):
            result = users.dist_by_num_of_ratings()
            assert isinstance(result, dict), "Result should be a dictionary"
            assert all(
                isinstance(title, str) for title in result.keys()
            ), "User id should be a string"
            assert all(
                isinstance(counts, int) for counts in result.values()
            ), "Count of ratings should be a int"
            sorted_by_counts = sorted(result.items(), key=lambda x: x[1], reverse=True)
            assert (
                list(result.items()) == sorted_by_counts
            ), "Result should be sorted by counts of rating descending"

        def test_dist_by_ratings(self, users):
            result = users.dist_by_ratings()
            assert isinstance(result, dict), "Result should be a dictionary"
            assert all(
                isinstance(title, str) for title in result.keys()
            ), "User id should be a string"
            assert all(
                isinstance(ratings, float) for ratings in result.values()
            ), "Rating should be a float"
            sorted_by_ratings = sorted(result.items(), key=lambda x: x[1], reverse=True)
            assert (
                list(result.items()) == sorted_by_ratings
            ), "Result should be sorted by rating descending"

        def test_top_controversial(self, users):
            result = users.top_controversial(5)
            assert isinstance(result, dict), "Result should be a dictionary"
            assert all(
                isinstance(title, str) for title in result.keys()
            ), "User id should be a string"
            assert all(
                isinstance(ratings, float) for ratings in result.values()
            ), "Variance of rating should be a float"
            sorted_by_ratings = sorted(result.items(), key=lambda x: x[1], reverse=True)
            assert (
                list(result.items()) == sorted_by_ratings
            ), "Result should be sorted by variance of rating descending"
