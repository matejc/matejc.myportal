from plone import api

__docformat__ = "epytext"


def runCustomCode(site):
    """ Run custom add-on product installation code
    to modify Plone site object and others

    @param site: Plone site
    """
    if not api.group.get(groupname="staff"):
        api.group.create(
            groupname="staff",
            title="Staff",
            roles=['Reader'],
        )

    blogs_folder = api.content.get(path="/blogs")

    #if blogs_folder:                        # TODO: FOR DEBUG ONLY!!
    #    print "deleting blogs folder to re-add it"
    #    api.content.delete(blogs_folder)
    #    blogs_folder = None

    if not blogs_folder:
        blogs_folder = api.content.create(
            type="Folder",
            title="Blogs",
            id="blogs",
            container=site,
        )

    # grant roles right after creation of context
    api.group.grant_roles(
        groupname="staff",
        obj=site["blogs"],
        roles=['Reader', 'Contributor', 'Editor', 'Reviewer'],
    )

    try:
        api.content.get(path="/blogs/myblog")
    except AttributeError:
        api.content.create(
            type="Collection",
            title="MyBlog",
            id="myblog",
            container=site['blogs']
        )
        myblog_coll = api.content.get(path="/blogs/myblog")
        query = [{
            'i': 'Type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Blog Entry',
        }]
        myblog_coll.setQuery(query)

        api.content.create(
            type="Blog Entry",
            title="MyBlogEntry",
            id="myblogentry",
            container=myblog_coll
        )


def setupVarious(context):
    """
    @param context:
        Products.GenericSetup.context.DirectoryImportContext instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('matejc.myportal.marker.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()

    runCustomCode(portal)
