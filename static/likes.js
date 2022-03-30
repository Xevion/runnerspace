function like(id) {
    $.ajax({url: `/post/${id}/like`, method: "POST", dataType: "json"})
        .done(function (data) {
            let post_parent = $(`#post-${id}`)
            let heart_icon = post_parent.find('.fa-heart')
            let pre_liked = heart_icon.hasClass('liked')

            // Toggle if the current state no longer matches the database state.
            if (pre_liked !== data.liked) {
                if (pre_liked)
                    heart_icon.removeClass('liked')
                else
                    heart_icon.addClass('liked')
            }

            // Set new state of the like status text
            post_parent.find('.post-like-status').html(data.status_text)
        })
}
