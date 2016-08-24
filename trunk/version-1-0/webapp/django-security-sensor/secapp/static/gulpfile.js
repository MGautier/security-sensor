var gulp = require('gulp');
var nanoCSS = require('gulp-cssnano');
var uglify = require('gulp-uglify');


gulp.task('cssnano', function(){
  return gulp.src('css/main.css')
    .pipe(nanoCSS())
    .pipe(gulp.dest('build/css/main.min.css'));
});

gulp.task('uglify', function(){
  return gulp.src('js/Visualizations.js')
    .pipe(uglify())
    .pipe(gulp.dest('build/js/Visualizations.min.js'));
});

gulp.task('optimized', ['cssnano', 'uglify']);
